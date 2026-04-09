import socket
import ssl
import sys
import threading
from queue import Queue

# --- Configuration ---
# Let's hire 100 workers for our crew. You can adjust this.
THREAD_COUNT = 100
# A lock to ensure that our print statements don't overlap and get jumbled
print_lock = threading.Lock()

def scan_port(port, target_name, target_ip, context):
    """
    This function contains the logic to scan a single port.
    It's what each of our worker threads will execute.
    """
    try:
        plain_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        plain_socket.settimeout(1.5)

        if plain_socket.connect_ex((target_ip, port)) == 0:
            banner = ""
            try:
                # --- The same probing logic as before ---
                if port in [443, 8443, 4433]: # SSL/TLS Port
                    secure_socket = context.wrap_socket(plain_socket, server_hostname=target_name)
                    probe = f'HEAD / HTTP/1.1\r\nHost: {target_name}\r\n\r\n'.encode()
                    secure_socket.sendall(probe)
                    response = secure_socket.recv(1024).decode(errors='ignore')
                    for line in response.split('\r\n'):
                        if 'server:' in line.lower(): banner = line.strip(); break
                    secure_socket.close()
                elif port in [80, 8080]: # HTTP Port
                    probe = f'HEAD / HTTP/1.1\r\nHost: {target_name}\r\n\r\n'.encode()
                    plain_socket.sendall(probe)
                    response = plain_socket.recv(1024).decode(errors='ignore')
                    for line in response.split('\r\n'):
                        if 'server:' in line.lower(): banner = line.strip(); break
                else: # Passive Banner Grab
                    banner = plain_socket.recv(1024).decode(errors='ignore').strip()
                
                # --- Thread-Safe Printing ---
                with print_lock:
                    print(f"Port {port}: OPEN")
                    if banner:
                        print(f"  [+] {banner}")
            except Exception:
                # Catch exceptions during probing but still report the port as open
                with print_lock:
                    print(f"Port {port}: OPEN (Probe failed)")
            finally:
                plain_socket.close()

    except (socket.timeout, ConnectionResetError, OSError):
        # These errors are expected for closed/filtered ports, so we pass silently.
        pass
    finally:
        plain_socket.close()


def worker(q, target_name, target_ip, context):
    """The function each worker thread runs."""
    while not q.empty():
        port = q.get()
        scan_port(port, target_name, target_ip, context)
        q.task_done()


def main():
    # --- Get User Input ---
    target_name = input("Enter target to scan (e.g., scanme.nmap.org): ")
    port_range_str = input("Enter port range to scan (e.g., 1-1000): ")
    
    try:
        target_ip = socket.gethostbyname(target_name)
        start_port, end_port = map(int, port_range_str.split('-'))
    except (socket.gaierror, ValueError):
        print("Invalid target or port range. Exiting.")
        sys.exit()

    # --- Setup ---
    print("-" * 50)
    print(f"Scanning {target_name} ({target_ip}) with {THREAD_COUNT} threads...")
    print("-" * 50)
    
    # Create the SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Create the job queue and fill it with ports
    q = Queue()
    for port in range(start_port, end_port + 1):
        q.put(port)

    # --- Start the Workers ---
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=worker, args=(q, target_name, target_ip, context), daemon=True)
        thread.start()

    # --- Wait for all jobs to be completed ---
    q.join()
    print("-" * 50)
    print("Scan complete.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan cancelled by user.")
        sys.exit()