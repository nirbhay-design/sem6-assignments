import sys
import socket

serversoc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

if (len(sys.argv) != 2):
    print(f"input format: python3 {sys.argv[0]} <PORT>")
    exit()

PORT= int(sys.argv[1])

serversoc.bind(('127.0.0.1',PORT))

serversoc.listen(5) # listen means you need to listen only 5 clients


while 1:
    print('server waiting for connection')
    cli,cli_addr = serversoc.accept()
    print(f'{cli_addr[0]}:{cli_addr[1]} connected successfully')

    while 1:
        data = cli.recv(2048) # 1024 bytes
        if not data or data.decode('utf-8') =='end':
            break;
        
        print('client\'s response: ',data.decode('utf-8'))
        try:
            # print(expr.split('+'))
            result = input("send msg to client: ")
            # print("printing the result" , result)
        except:
            result = "error"
        # server_res = input('give response: ')
        cli.send(str(result).encode())

    cli.close()

serversoc.close()

