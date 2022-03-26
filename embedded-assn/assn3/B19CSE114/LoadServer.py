import os
import sys as system

if (system.argv.__len__() < 4):
    print(f'input format is : python3 {system.argv[0]} <ip> <PORT> <Iterations>')
    exit(0);

ip = system.argv[1]
port = system.argv[2];
iterations = int(system.argv[3])
for i in range(iterations):
    os.system(f'python3 client.py {ip} {port}')
    