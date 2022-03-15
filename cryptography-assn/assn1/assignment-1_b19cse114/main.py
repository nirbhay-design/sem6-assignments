import numpy as np
from collections import Counter
import math
l = []

with open('v_ciphertext_74.txt') as f:
    l.append(f.read())

cipher = l[0]
# cipher = "yymranvrzvfugualbeqlvhmdpegwrmdrblfmifvxedrrbmlvkkplbqgpmwzkqjmhxfczvwqsjvumaccpaykvcbmymrnvmtvggrlwedeccghdfcqobzpfthed"
# cipher = "VVHQWVVRMHUSGJG"
# print(cipher)


"""
Approach for cracking:

the apprach is simple first find the key length
then find the key 
and then decrypt the text

for finding the key length I have first tried to find out the occurances that are repeating
then I got an idea that my key length is around 5 chars 
then I divide my text into that(key) length batches 
then took first char from each batch and find the peak and subtract it with 'e' so as to get the first char of key
similarly got rest other characters and then decrypt the text 

but unfortunately it didn't work for me for keylength 5 so I tried for 6 and it got decrypted successfully

"""

freq = dict(list(zip('abcdefghijklmnopqrstuvwxyz',[
    8.2,
    1.5,
    2.8,
    4.3,
    12.7,
    2.2,
    2.0,
    6.1,
    7,
    0.2,
    0.8,
    4,
    2.4,
    6.7,
    1.5,
    1.9,
    0.1,
    6,
    6.3,
    9.1,
    2.8,
    1.0,
    2.4,
    0.2,
    2,
    0.1
])))

d = dict(list(zip('abcdefghijklmnopqrstuvwxyz',list(range(26)))))
d1 = {i:j for j,i in list(d.items())}
def dec(cipher,k):
    
    n = len(cipher)
    m = len(k)
    a,b = n//m, n%m
    updated_key = k*a + k[:b]
    assert len(updated_key) == n
    pt = ""
    for i,j in enumerate(cipher):
        pt += d1[(d[j] - d[updated_key[i]]+26)%26]
    return pt;



def rightshift(arr,k):
    n:int = len(arr)
    return arr[k%n:] + arr[0:k%n] 


def getrotnum(arr1,arr2):
    assert len(arr1) == len(arr2),"length of both the arrays should be same"
    val = []
    j:int = 0
    while(j<len(arr2)):
        arr22 = rightshift(arr2,j)
        arr = np.sum(np.array(arr1) * np.array(arr22))
        val.append((arr,j))
        j+=1
    
    ix = -1;
    mx = -math.inf
    for idx,thing in enumerate(val):
        if (thing[0] > mx):
            mx = thing[0]
            ix = thing[1]
    # print(val)
    return ix;
    

def freqanalysis(text):
    a = Counter(text)
    val = sorted(list(a.items()),key = lambda x:x[1],reverse=True)
    val1 = sorted(list(freq.items()),key=lambda x:x[1],reverse=True)
    final_dict = {}
    for idx,i in enumerate(val):
        final_dict[i[0]]=val1[idx][0]

    atext = ""
    for i in range(len(text)):
        atext += final_dict[text[i]]

    print(atext)   
        

def findkey(cipher):
    key = ""
    n = len(cipher)
    numarr = []
    index = 1
    while (index < n):
        nl = 0;
        for i in range(0,n-index):
            if (cipher[i] == cipher[i+index]):
                nl += 1
        numarr.append(nl)
        index += 1

    # numarr = np.array(numarr)
    # print(numarr)
    newarr = sorted(list(zip(numarr,list(range(0,len(numarr))))),key=lambda x:x[0],reverse=True)
    # print(newarr)

    # idxarr = []
    # avg = np.average(numarr)
    # for idx,value in enumerate(numarr):
    #     if (value > avg):
    #         idxarr.append(idx)
    # observe and get keylen = 25
    # difference = []
    keylen = 6
    # doing the simple frequency analysis
    split_cipher = [cipher[i:i+keylen] for i in range(0,len(cipher),keylen)]
    if (keylen != len(split_cipher[-1])):
        split_cipher = split_cipher[:-1]
    keyvalue = ""
    t = 0
    while (t<keylen):
        tmpstr = ""
        for m in split_cipher:
            tmpstr += m[t]
        der = dict(Counter(tmpstr))
        maxval= -math.inf
        desiredchar= ''
        for i,j in list(der.items()):
            if j > maxval:
                maxval = j
                desiredchar = i
        keyvalue += d1[(ord(desiredchar)-ord('e')+26)%26]
        t+=1

    return keyvalue;

def encr(pt,key):
    d = dict(list(zip('abcdefghijklmnopqrstuvwxyz',list(range(26)))))
    d1 = {i:j for j,i in list(d.items())}
    n = len(pt)
    m = len(key)
    a,b = n//m, n%m
    updated_key = key*a + key[:b]
    print(updated_key)
    cipher = ""
    for i,j in enumerate(pt):
        cipher += d1[(d[j] + d[updated_key[i]])%26]
    return cipher;


def main():
    key=findkey(cipher)
    print(key)
    print(dec(cipher,key))    

main();
# freqanalysis(cipher)
# print(getrotnum([1,2,3,4],[2,1,5,4]))