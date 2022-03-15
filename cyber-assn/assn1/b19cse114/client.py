import sys
import socket

if (len(sys.argv) < 3):
    print(f"Input format: {sys.argv[0]} <IP> <PORT>")
    exit()

mysocket = socket.socket()


IP = sys.argv[1]
PORT = int(sys.argv[2])

mysocket.connect((IP,PORT))

while 1:
    a = input("enter msg to server: ")
    mysocket.send(a.encode())

    b = mysocket.recv(2048)
    print("server replied: ",b.decode('utf-8'))
    

mysocket.close()