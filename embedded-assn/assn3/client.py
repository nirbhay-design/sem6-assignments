import sys
import socket
import time

if (len(sys.argv) < 3):
    print("port and ip both are required! please try again")
    exit()

mysocket = socket.socket()


IP = sys.argv[1]
PORT = int(sys.argv[2])

mysocket.connect((IP,PORT))


mysocket.send(str([1,2,3,4,5,6,7,8,9]).encode())
received = mysocket.recv(1024).decode()

# time.sleep(10)
mysocket.close()