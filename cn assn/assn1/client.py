import sys
import socket

if (len(sys.argv) < 3):
    print("port and ip both are required! please try again")
    exit()

mysocket = socket.socket()


IP = sys.argv[1]
PORT = int(sys.argv[2])

mysocket.connect((IP,PORT))

while 1:
    print(mysocket.recv(1024).decode())
    

mysocket.close()