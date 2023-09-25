import telnetlib
import socket

def check_smtp_capabilities(host, hostname):
    try:
        # Resolve the hostname to an IP address
        ip_address = socket.gethostbyname(host)
        print(f"Checking SMTP capabilities for {ip_address} ({host}) using EHLO {hostname}")

        # Connect to the SMTP server on port 25
        with telnetlib.Telnet(host, 25) as tn:
            # Receive the server's banner message
            banner = tn.read_until(b"\r\n", timeout=5).decode("utf-8")
            print(f"Received banner for {ip_address} ({host}): {banner.strip()}")

            # Send EHLO command followed by the hostname
            ehlo_command = f"EHLO {hostname}\r\n"
            tn.write(ehlo_command.encode("utf-8"))

            # Receive and print the server's response
            response = tn.read_until(b"\r\n", timeout=5).decode("utf-8")
            print(response.strip())

            # Indicate that this host worked
            return ip_address

    except Exception as e:
        print(f"Failed to connect to {ip_address} ({host}): {str(e)}")
        # Indicate that this host did not work
        return None

# Read the list of hostnames from a file
hosts_file = "hosts.txt"
with open(hosts_file, "r") as file:
    hosts = [line.strip() for line in file]

# Hostname to announce in the EHLO command
my_hostname = "myhostname.com"

# List to store the IP addresses of working hosts
working_ips = []

# Loop through each host and check SMTP capabilities
for host in hosts:
    result = check_smtp_capabilities(host, my_hostname)
    if result:
        working_ips.append(result)
    print("----------------------------------------------")

# Print the list of working IP addresses
print("Working IP Addresses:")
for ip in working_ips:
    print(ip)
