import socket
import sys

# --- Configuration ---
try:
    # Use socket.gethostbyname to handle both IPs and domain names
    target_ip = socket.gethostbyname(input("Enter target to scan (e.g., scanme.nmap.org): "))
except socket.gaierror:
    print("Error: Invalid hostname. Exiting.")
    sys.exit()

# Get port range from user
try:
    start_port, end_port = map(int, input("Enter port range (e.g., 20-85): ").split('-'))
except ValueError:
    print("Error: Invalid port range format. Use START-END. Exiting.")
    sys.exit()

print("-" * 50)
print(f"Scanning target: {target_ip}")
print(f"Port Range: {start_port}-{end_port}")
print("-" * 50)

# --- The Scanner Logic ---
try:
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0) # A slightly longer timeout might be needed to receive a banner

        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            banner = ""
            try:
                # If port is open, try to receive 1024 bytes of data
                # This is the "banner grabbing" part
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except socket.timeout:
                # If we time out waiting for a banner, that's okay
                banner = "No banner received (Timeout)"
            except ConnectionResetError:
                banner = "Connection reset by peer."
            except Exception:
                banner = "Could not retrieve banner"
            
            print(f"Port {port}: OPEN")
            if banner:
                # Print the banner on a new, indented line
                print(f"  [+] Banner: {banner}")
        
        # We always close the socket when we're done with the port
        s.close()

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()
except Exception as e:
    print(f"An unhandled error occurred: {e}")
    sys.exit()