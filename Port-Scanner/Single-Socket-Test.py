import socket

# --- Configuration ---
# We'll use a target that is safe to scan for educational purposes.
# scanme.nmap.org is a service explicitly provided for this.
target_ip = 'scanme.nmap.org' 
target_port = 80 # Let's check the standard web port

# --- The Scanner Logic ---
try:
    # 1. Create a socket object
    # AF_INET specifies we're using IPv4
    # SOCK_STREAM specifies this is a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Set a timeout. This is crucial! If a port is filtered or slow,
    #    we don't want our script to hang forever. 1 second is reasonable.
    s.settimeout(1.0)

    # 3. Attempt to connect. 
    #    connect_ex() is better than connect() for scanning. It returns an
    #    error code instead of raising an exception if it fails.
    #    A return code of 0 means the connection was successful.
    result = s.connect_ex((target_ip, target_port))

    # 4. Check the result
    if result == 0:
        print(f"Port {target_port} is OPEN")
    else:
        # The result will be a non-zero error number if the port is closed
        print(f"Port {target_port} is CLOSED")

except socket.gaierror:
    # This error happens if the hostname could not be resolved.
    print(f"Error: Hostname '{target_ip}' could not be resolved.")
except Exception as e:
    # Catch any other exceptions
    print(f"An error occurred: {e}")
finally:
    # 5. Always close the socket
    s.close()