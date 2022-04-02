import os
import subprocess
if (os.path.exists('whois_data.txt')):
    os.remove('whois_data.txt')
with open('a.txt') as f:
    for line in f.readlines():
        ip = line.split(',')[0][2:-1]
        ases = line.split(',')[-1][2:-3].split(' ')[0]
        # print(ases)
        text = '#'*25 +f' ip address {ip} ' + '#'*25
        res1 = subprocess.getoutput(f'whois {ip} | grep -iE "Network Name|NetName|netname"')
        res2 = subprocess.getoutput(f'echo ases_value: {ases}')
        with open('whois_data.txt','a') as ff:
            ff.write(text + '\n')
            if (res1 == ""):
                ff.write('cannot query at this time \n')
            else:
                ff.write(res1 + '\n')
            ff.write(res2 + '\n\n')

        # os.system(f'whois {ip} | grep -iE "Network Name|NetName|netname"')
        # os.system(f'echo ases_value: {ases}')