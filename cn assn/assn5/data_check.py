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

reg = r'(103\.21\.12[4-7]\.\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\b/24)'

lines = return_file('bgp-routing-table.txt')

t1 = time.perf_counter()

n_values = 16048103

values_idx = {'prefix':5,'type':0,'time':1,'baw':2,'fip':3,'fas':4,'aspath':6}
set_pref = set()
set_as = set()
set_a = set()

for idx,line in enumerate(lines):
    entries = line.split('|')
    set_pref.add(entries[values_idx['prefix']])
    set_as.add(entries[values_idx['fas']])
    # ips = re.findall(reg,entries[values_idx['prefix']])
    # if (len(ips) != 0):
        # set_a.add((entries[values_idx['prefix']],entries[values_idx['aspath']]))

    pref = entries[values_idx['prefix']]
    if (pref[-2:] == '24'):
        pref = pref[:-3]
        values = list(map(lambda x:int(x),pref.split('.')))
        if values[0] == 103 and values[1] == 21 and (values[2] <= 127 and values[2] >= 124) and (values[3] >= 0 and values[3] <= 255):
            set_a.add((entries[values_idx['fip']],entries[values_idx['prefix']],entries[values_idx['aspath']]))


print(f'unique prefix: {len(set_pref)}')
print(f'unique as: {len(set_as)}')
print(f'entries in set A: {len(set_a)}')

write_to_file('unique_prefix.txt',set_pref)
write_to_file('unique_as.txt',set_as)
write_to_file('a.txt',set_a)

t2 = time.perf_counter()

print(f'completed in {(t2-t1):.3f} Sec')
exit(0)

