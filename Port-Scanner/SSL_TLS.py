import socket
import ssl
import sys

def get_target_and_ports():
    """Gets target IP and port range from the user."""
    try:
        target_name = input("Enter target to scan (e.g., google.com): ")
        target_ip = socket.gethostbyname(target_name)
    except socket.gaierror:
        print("Error: Invalid or unreachable hostname. Exiting.")
        sys.exit()

    try:
        port_range_str = input("Enter port range (e.g., 80-443): ")
        start_port, end_port = map(int, port_range_str.split('-'))
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
            raise ValueError("Invalid port numbers.")
    except ValueError:
        print("Error: Invalid port range format. Use START-END with ports between 1 and 65535. Exiting.")
        sys.exit()
        
    return target_name, target_ip, start_port, end_port

def main():
    target_name, target_ip, start_port, end_port = get_target_and_ports()

    # Create a default SSL context once, outside the loop
    # We will disable certificate validation for our scanner's purposes
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    print("-" * 50)
    print(f"Scanning Target: {target_name} ({target_ip})")
    print("-" * 50)

    for port in range(start_port, end_port + 1):
        # Use a new plain socket for each port
        plain_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        plain_socket.settimeout(1.5)

        if plain_socket.connect_ex((target_ip, port)) == 0:
            print(f"Port {port}: OPEN")
            banner = ""
            try:
                # --- SSL/TLS WRAPPING LOGIC ---
                if port in [443, 8443, 4433]:
                    # This is an SSL port, wrap the socket
                    secure_socket = context.wrap_socket(plain_socket, server_hostname=target_name)
                    probe = f'HEAD / HTTP/1.1\r\nHost: {target_name}\r\n\r\n'.encode()
                    secure_socket.sendall(probe)
                    response = secure_socket.recv(1024).decode(errors='ignore')
                    # Parse for Server header
                    for line in response.split('\r\n'):
                        if 'server:' in line.lower():
                            banner = line.strip()
                            break
                    secure_socket.close() # Close the secure socket
                
                # --- HTTP PROBING (Unchanged) ---
                elif port in [80, 8080]:
                    probe = f'HEAD / HTTP/1.1\r\nHost: {target_name}\r\n\r\n'.encode()
                    plain_socket.sendall(probe)
                    response = plain_socket.recv(1024).decode(errors='ignore')
                    for line in response.split('\r\n'):
                        if 'server:' in line.lower():
                            banner = line.strip()
                            break
                
                # --- PASSIVE BANNER GRABBING (Unchanged) ---
                else:
                    banner = plain_socket.recv(1024).decode(errors='ignore').strip()
                
                if banner:
                    print(f"  [+] {banner}")

            except (socket.timeout, ConnectionResetError) as e:
                print(f"  [!] Could not get banner: {e}")
            except ssl.SSLError as e:
                print(f"  [!] SSL Error: {e}. The service might not be HTTPS.")
            finally:
                # The plain socket is closed here, as it's outside the secure_socket scope
                plain_socket.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan cancelled by user.")
        sys.exit()