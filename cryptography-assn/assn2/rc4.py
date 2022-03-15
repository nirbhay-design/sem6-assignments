import random
from collections import Counter
s = [0]*256

def ksa(n,k):
    global s
    for i in range(0,256):
        s[i] = i
    key = [int(k[i:i+n],2) for i in range(0,len(k),n)]
    
    if (len(key) < 256):
        m = 0
        while (len(key)!=256):
            key.append(key[m])
            m += 1
    j = 0
    for i in range(0,256):
        j = (j + s[i] + key[i]) % 256
        s[i],s[j] = s[j], s[i]

    i = 0;j = 0
    return s

def prga():
    global s
    # print(s)
    i = 0;j = 0
    key = []
    while (i < 4):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[i], s[j]
        t = (s[i] + s[j]) % 256
        keystreambyte = s[t]
        key.append(keystreambyte)
    return key

def randomkeygen(n):
    d = ['0','1']
    ky = ""
    for i in range(n):
        ky += random.choice(d)
    return ky
# print(ksa(3,'101001000001'))
# print(ksa(4,'101001000001'))
# print(prga())

# key = prga()
# secondbyte = []
# for i in range(10000):
#     # print(i)
#     n = (i + 20) % 256 
#     if n <= 4:
#         n = 4
#     k = randomkeygen(n)
#     choices_for_n = [2,3,4,5,6,7,8]
#     finaln = random.choice(choices_for_n)
#     # print(n,k,finaln)
#     ksa(finaln,k)
#     key = prga()
#     secondbyte.append(key[2])

# print(Counter(secondbyte))

for i in range(1000):
    print(random.randint(1,256))