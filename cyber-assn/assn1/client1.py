import socket 
import sys

if len(sys.argv) < 3:
    print(f"input format: {sys.argv[0]} <URL> <PORT>")
    exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

url = sys.argv[1]
port = int(sys.argv[2])
 
try:
    HostIp = socket.gethostbyname(url)
except Exception as e:
    print(e)
 
s.connect((HostIp, port))
 
print(f"connected to {url} on ip {HostIp}")