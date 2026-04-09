import socket
import sys

def get_target_and_ports():
    """Gets target IP and port range from the user."""
    try:
        # Resolve hostname to IP address
        target_name = input("Enter target to scan (e.g., scanme.nmap.org): ")
        target_ip = socket.gethostbyname(target_name)
    except socket.gaierror:
        print("Error: Invalid or unreachable hostname. Exiting.")
        sys.exit()

    try:
        port_range_str = input("Enter port range (e.g., 20-100): ")
        start_port, end_port = map(int, port_range_str.split('-'))
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
            raise ValueError("Invalid port numbers.")
    except ValueError:
        print("Error: Invalid port range format. Use START-END with ports between 1 and 65535. Exiting.")
        sys.exit()
        
    return target_name, target_ip, start_port, end_port

def main():
    target_name, target_ip, start_port, end_port = get_target_and_ports()

    print("-" * 50)
    print(f"Scanning Target: {target_name} ({target_ip})")
    print("-" * 50)

    # --- Scanner Logic ---
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)

        if s.connect_ex((target_ip, port)) == 0:
            try:
                banner = ""
                # --- ACTIVE PROBING LOGIC ---
                if port == 80 or port == 8080:
                    # It's a web port, let's send an HTTP HEAD request
                    probe = f'HEAD / HTTP/1.1\r\nHost: {target_name}\r\n\r\n'.encode()
                    s.sendall(probe)
                    response = s.recv(1024).decode(errors='ignore')
                    # Find the 'Server' header in the response for a clean output
                    for line in response.split('\r\n'):
                        if 'server:' in line.lower():
                            banner = line.strip()
                            break
                    if not banner:
                        banner = "HTTP Response (No Server Header)"
                else:
                    # It's not a web port, just listen passively
                    banner = s.recv(1024).decode(errors='ignore').strip()
                
                print(f"Port {port}: OPEN")
                if banner:
                    print(f"  [+] {banner}")

            except (socket.timeout, ConnectionResetError):
                # If the port closes before we get data, that's fine.
                print(f"Port {port}: OPEN (No response to probe)")
            finally:
                s.close()
        else:
            s.close() # Close the socket if connect_ex failed

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan cancelled by user.")
        sys.exit()