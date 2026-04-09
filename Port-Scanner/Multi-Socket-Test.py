import socket
import sys

# --- Configuration ---
# Get the target from user input
try:
    target_ip = socket.gethostbyname(input("Enter target to scan (e.g., scanme.nmap.org): "))
except socket.gaierror:
    print("Error: Invalid hostname. Exiting.")
    sys.exit()

print("-" * 50)
print(f"Scanning target: {target_ip}")
print("-" * 50)

# --- The Scanner Logic ---
try:
    # We will scan ports 1 through 100
    for port in range(1, 101):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # A shorter timeout for faster scanning

        result = s.connect_ex((target_ip, port))
        
        # If the port is open, print it. We don't need to see the closed ones.
        if result == 0:
            print(f"Port {port}: OPEN")
        
        s.close()

except KeyboardInterrupt:
    # Allows us to press Ctrl+C to exit gracefully
    print("\nExiting program.")
    sys.exit()
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit()