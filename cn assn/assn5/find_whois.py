import os
with open('a.txt') as f:
    for line in f.readlines():
        ip = line.split(',')[0][2:-1]
        ases = line.split(',')[-1][2:-3].split(' ')[0]
        # print(ases)
        print('#'*25 +f' ip address {ip} ' + '#'*25)
        os.system(f'whois {ip} | grep -iE "Network Name|NetName|netname"')
        os.system(f'echo ases_value: {ases}')