import sys
import socket

serversoc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

if (len(sys.argv) != 2):
    print(f"input format: python3 {sys.argv[0]} <PORT>")
    exit()

PORT= int(sys.argv[1])

serversoc.bind(('127.0.0.1',PORT))

serversoc.listen(5) # listen means you need to listen only 5 clients


def evaluate_expr(expr):
    operator = ""
    result = 0
    dict1 = {-6:'*',-5:'+',-3:'-',-1:'/',-16:' '}
    error = False
    for i in range(len(expr)):
        ascidif = ord(expr[i]) - ord('0')
        if ascidif < 0:
            if dict1.get(ascidif,-1) == -1:
                error = True
            else:
                if (operator == ""):
                    operator = (lambda x: x if x != ' ' else "")(dict1[ascidif])

    if (error or operator == ""):
        return "error"
    else:
        if (expr.split(operator).__len__() != 2):
            return "error"
        operand_values = list(map(lambda x:int(x.strip()) if x.strip().isdigit() else "",list(expr.split(operator))))
        if (any([i == '' for i in operand_values])):
            return 'error'
        functions = {'*':int.__mul__,'-':int.__sub__,'/':int.__truediv__,'+':int.__add__}
        result =   functions[operator](operand_values[0],operand_values[1])
        return str(result)


while 1:
    print('server waiting for connection')
    cli,cli_addr = serversoc.accept()
    print(f'{cli_addr[0]}:{cli_addr[1]} connected successfully')

    while 1:
        data = cli.recv(1024) # 1024 bytes
        if not data or data.decode('utf-8') =='end':
            break;
        
        print('client\'s query: ',data.decode('utf-8')[:-1])
        expr = data.decode('utf-8')
        expr = expr[:-1]
        try:
            # print(expr.split('+'))
            result = evaluate_expr(expr)
            # print("printing the result" , result)
        except:
            result = "error"
        # server_res = input('give response: ')
        cli.send(str(result).encode())

    cli.close()

serversoc.close()

