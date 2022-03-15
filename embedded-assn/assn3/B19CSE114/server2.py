import sys
import socket
import threading
from threading import Thread
import time

serversoc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

if (len(sys.argv) != 2):
    print(f"input format: python3 {sys.argv[0]} <PORT>")
    exit()

PORT= int(sys.argv[1])

serversoc.bind(('127.0.0.1',PORT))
serversoc.listen()

def evaluate_expr(expr):
    return expr
    res = 0
    for i in range(len(expr)):
        res *= expr[i]
    return f'{res}'

def contact(cli,addr):

    while 1:
        data = cli.recv(1024) # 1024 bytes
        if not data or data.decode('utf-8') =='end':
            break;

        print(f'{addr[0]}:{addr[1]}\'s query: ',data.decode('utf-8'))
        expr = data.decode('utf-8')
        # expr = expr[:-1]
        try:
            result = evaluate_expr(expr)
        except:
            result = "error"
        # server_res = input('give response: ')
        cli.send(str(result).encode())

    time.sleep(10)
    cli.close()
    print(f'{addr[0]}:{addr[1]} leaves')


while 1:
    print('server waiting for connection')
    cli,address = serversoc.accept()
    t1 = Thread(target = contact,args=(cli,address))
    t1.start()
    print(f'{address[0]}:{address[1]} joined successfully')
    print('total connections ', threading.activeCount()-1)

serversoc.close()

