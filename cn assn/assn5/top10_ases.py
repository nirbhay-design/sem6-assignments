import os
import subprocess
# import re
if (os.path.exists('whois_top10.txt')):
    os.remove('whois_top10.txt')
with open('top_10_ases.txt') as f:
    for line in f.readlines():
        if ('{' not in line):continue;

        list_break = list(map(lambda x:x.strip(),line.split(',')))
        ases = list_break[-2][1:-1]
        ip_s = []
        for various_ip in list_break[:-2]:
            if ('{' in various_ip):
                if ('}' in various_ip):
                    ip_s.append(various_ip[3:-2])
                else:
                    ip_s.append(various_ip[3:-1])
            elif ('}' in various_ip):
                ip_s.append(various_ip[1:-2])
            else:
                ip_s.append(various_ip[1:-1])
        # print(ip_s)
        for ip in ip_s:
            # print(ases)
            text = '#'*25 +f' ip address {ip} ' + '#'*25
            res1 = subprocess.getoutput(f'whois {ip} | grep -iE "Network Name|NetName|netname"')
            res2 = subprocess.getoutput(f'echo ases_value: {ases}')
            with open('whois_top10.txt','a') as ff:
                ff.write(text + '\n')
                if (res1 == ""):
                    ff.write('cannot query at this time \n')
                else:
                    ff.write(res1 + '\n')
                ff.write(res2 + '\n\n')

            # os.system(f'whois {ip} | grep -iE "Network Name|NetName|netname"')
            # os.system(f'echo ases_value: {ases}')