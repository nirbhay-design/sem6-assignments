import os
import time
# import re

def write_to_file(file_name,data):
    if (os.path.exists(file_name)):
        os.remove(file_name)
    with open(file_name,'a') as f:
        for values in data:
            f.write(str(values) + '\n')

def return_file(file_name):
    with open (file_name,'r') as f:
        for line in f.readlines():
            yield line

def find_instia_buysnetworkservicefrom():
    with open('a.txt') as f:
        st = set()
        for line in f.readlines():
            # ip = line.split(',')[0][2:-1]
            ases = line.split(',')[-1][2:-3].split(' ')
            for i in range(len(ases)):
                if ases[i] == ases[-1]:
                    st.add(ases[i-1])
                    break;
    return st;

reg = r'(103\.21\.12[4-7]\.\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\b/24)'

lines = return_file('bgp-routing-table.txt')

t1 = time.perf_counter()

n_values = 16048103

values_idx = {'prefix':5,'type':0,'time':1,'baw':2,'fip':3,'fas':4,'aspath':6}
set_pref = set()
set_as = set()
set_a = set()
top_10_ases = {}
# ases_ip_map = {}

print(f'\nplease wait it will take a while (around 5 Mins) ')

for idx,line in enumerate(lines):
    entries = line.split('|')
    set_pref.add(entries[values_idx['prefix']])
    set_as.add(entries[values_idx['fas']])
    # ips = re.findall(reg,entries[values_idx['prefix']])
    # if (len(ips) != 0):
        # set_a.add((entries[values_idx['prefix']],entries[values_idx['aspath']]))
    pref = entries[values_idx['prefix']]
    if (pref[-2:] == '24'):
    # pref = pref[:-3]
        pref = pref.split('/')[0]
        values = list(map(lambda x:int(x),pref.split('.')))
        if values[0] == 103 and values[1] == 21 and (values[2] <= 127 and values[2] >= 124) and (values[3] >= 0 and values[3] <= 255):
            set_a.add((entries[values_idx['prefix']],entries[values_idx['aspath']]))

    ases_path = entries[values_idx['aspath']].split(' ')
    # as__es = entries[values_idx['fas']]
    # if as__es not in ases_ip_map:
    #     ases_ip_map[as__es] = set();
    # ases_ip_map[as__es].add(entries[values_idx['fip']])
    if (len(ases_path) <= 1):
        continue
    for jdx,as_es in enumerate(ases_path):
        if (as_es not in top_10_ases):
            top_10_ases[as_es] = set()
        if (jdx == 0):
            top_10_ases[as_es].add(ases_path[jdx+1])
        elif (jdx == len(ases_path) - 1):
            top_10_ases[as_es].add(ases_path[jdx-1])
        else:
            top_10_ases[as_es].add(ases_path[jdx-1])
            top_10_ases[as_es].add(ases_path[jdx+1])

top10as = sorted(list(map(lambda x: (x[0],len(top_10_ases[x[0]])),top_10_ases.items())),key=lambda x:x[1], reverse=True)[:10]

# top10_values = list(map(lambda x: (x[0],x[1]),top10as))

from_isp = find_instia_buysnetworkservicefrom()


print(f'unique prefix: {len(set_pref)}')
print(f'unique as: {len(set_as)}')
print(f'entries in set A: {len(set_a)}')
print(f'entries insti-A buys network service from: {len(from_isp)}')


write_to_file('unique_prefix.txt',set_pref)
write_to_file('unique_as.txt',set_as)
write_to_file('a.txt',set_a)
write_to_file('whois_a.txt',from_isp)
write_to_file('top_10_ases.txt',top10as)

t2 = time.perf_counter()


print(f'completed in {(t2-t1):.3f} Sec')
exit(0)

'''
https://mxtoolbox.com/SuperTool.aspx?action=asn%3a55824&run=toolpage
unique prefix: 525483
unique as: 34        
entries in set A: 130
completed in 150.924 Sec
'''