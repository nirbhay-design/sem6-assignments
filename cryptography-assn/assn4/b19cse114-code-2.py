'''
NIRBHAY SHARMA (B19CSE114)
'''


def ddt(s):
    n = 3
    d = [[0] * 2**n for _ in range(2**n)]
    # print(len(d))
    # print(len(d[0]))
    for alph in range(2**n):
        for x in range(2**n):
            bet = s[x] ^ s[x ^ alph]
            d[alph][bet] += 1
    for i in range(len(d)):
        for j in range(len(d[0])):
            print(d[i][j],end=' ')
        print()

print('que1'+'-'*50)
ddt([6,5,1,0,3,2,7,4])

class SPN():
    def __init__(self,keys,sbox):
        self.keys = keys
        self.sbox = sbox
    
    def padkeys(self,key,lent):
        if (len(key) < lent):
            key = '0'*(lent-len(key)) + key
            return key
        return key
    
    def sbx(self,inp):
        return self.padkeys(bin(self.sbox[int(inp,2)])[2:],3)
    
    def mixedsubkey(self,x,k):
        val1 = int(x,2)
        val2 = int(k,2)
        val = val1 ^ val2
        return self.padkeys(bin(val)[2:],6)

    def shuffleinput(self,x1,x2):
        x = x1[0] + x2[:2] + x1[-2:] + x2[-1]
        return x

    def encrypt(self,x,showint_states = False):
        A = self.mixedsubkey(x,self.keys[0])
        B1 = self.sbx(A[:3])
        B2 = self.sbx(A[-3:])
        B = B1 + B2
        D = self.shuffleinput(B1, B2)
        E = self.mixedsubkey(D,self.keys[1])
        F1 = self.sbx(E[:3])
        F2 = self.sbx(E[-3:])
        F = F1 + F2
        G = self.shuffleinput(F1,F2)
        H = self.mixedsubkey(G,self.keys[2])
        J1 = self.sbx(H[:3])
        J2 = self.sbx(H[-3:])
        J = J1 + J2
        C = self.mixedsubkey(J,self.keys[3])
        self.H_state = H
        self.J_state = J
        if showint_states:
            print('A: ',A)
            print('B: ',B)
            print('D: ',D)
            print('E: ',E)
            print('F: ',F)
            print('G: ',G)
            print('H: ',H)
            print('J: ',J)
        return C

spn = SPN(("010101", "001011", "111000", "111110"),[6,5,1,0,3,2,7,4])
# spn = SPN(("011111", "111111", "111011", "111110"),[6,5,1,0,3,2,7,4])
print('que2'+'-'*50)
cipher_text = spn.encrypt("011010",True)
print("cipher_text: ",cipher_text)
def xor_strings(str1,str2):
    strr = ""
    for i in range(len(str1)):
        b1 = str1[i]
        b2 = str2[i]
        if (b1 == b2):
            strr += '0'
        else:
            strr += '1'
    return strr

def generate_all(t,p,p_dash,p_arr):
    if (len(t) ==0):
        p_arr.append((p,p_dash))
        return 

    bit = t[0]
    if bit == '0':
        p1 = p + '0'
        pdash1 = p_dash + '0'
        p2 = p + '1'
        pdash2 = p_dash + '1'
        generate_all(t[1:],p1,pdash1,p_arr)
        generate_all(t[1:],p2,pdash2,p_arr)

    else:
        p1 = p + '0'
        pdash1 = p_dash + '1'
        p2 = p + '1'
        pdash2 = p_dash + '0'
        generate_all(t[1:],p1,pdash1,p_arr)
        generate_all(t[1:],p2,pdash2,p_arr)

p_arr = []
p = ""
p_dash = ""
generate_all("000001",p,p_dash,p_arr)
p_array = set(map(lambda x:tuple(sorted(x,key=lambda x:x)),p_arr))

delta_h = set()
for i,j in p_array:
    spn.encrypt(i)
    H1 = spn.H_state
    spn.encrypt(j)
    H2 = spn.H_state
    H = xor_strings(H1,H2)
    delta_h.add(H)
print('que3'+'-'*50)
print(f'total delta-H possible are : {len(delta_h)}')
print(delta_h)

'''
j1_xor_j2 = xor_strings(c1_last3,c2_last3)
p_arr = []
generate_all(j1_xor_j2,"","",p_arr)
p_array = set(map(lambda x:tuple(sorted(x,key=lambda x:x)),p_arr))
possible_keys = set()
for i,j in p_array:
    possible_keys.add(xor_strings(c1_last3,i))
print(possible_keys)
'''

print('que4'+'-'*50)
class Attack:
    def __init__(self,s_map,delta_h):
        self.smap = {self.padkeys(bin(s_map[i])[2:],3):self.padkeys(bin(i)[2:],3) for i in range(len(s_map))}
        self.dh = delta_h
        self.possible_last3 = {i[-3:] for i in self.dh}
        self.possible_first3 = {i[:3] for i in self.dh}
        # print(self.possible_first3)
        # print(self.s_map)
    def attack_last3(self,plaintext,ciphertext):        
        p1,p2 = plaintext
        c1,c2 = ciphertext
        c1_last3 = c1[-3:]
        c2_last3 = c2[-3:]

        possible_keys = self.generate_subset(3)
        # print(possible_keys)
        final_last3 = set()
        for keyy in possible_keys:
            j1 = xor_strings(c1_last3,keyy)
            h1 = self.smap[j1]
            j2 = xor_strings(c2_last3,keyy)
            h2 = self.smap[j2]
            final_h = xor_strings(h1,h2)
            if (final_h in self.possible_last3):
                final_last3.add(keyy)

        # print('last 3 bits: ',final_last3)
        return final_last3
    def attack_first3(self,plaintext,ciphertext):
        # print(self.smap)
        p1,p2 = plaintext
        c1,c2 = ciphertext
        c1_first3 = c1[:3]
        c2_first3 = c2[:3]

        # j1_xor_j2 = xor_strings(c1_first3,c2_first3)
        # p_arr = []
        # generate_all(j1_xor_j2,"","",p_arr)
        # p_array = set(map(lambda x:tuple(sorted(x,key=lambda x:x)),p_arr))
        # possible_keys = set()
        # for i,j in p_array:
        #     possible_keys.add(xor_strings(c1_first3,i))
        # # print(possible_keys)
        possible_keys = self.generate_subset(3)
        final_first3 = set()
        for keyy in possible_keys:

            j1 = xor_strings(c1_first3,keyy)
            h1 = self.smap[j1]
            j2 = xor_strings(c2_first3,keyy)
            h2 = self.smap[j2]
            final_h = xor_strings(h1,h2)
            # print(keyy,final_h,j1,h1,j2,h2)
            if (final_h in self.possible_first3):
                final_first3.add(keyy)

        # print('first 3 bits: ',final_first3)
        return final_first3
    def padkeys(self,key,lent):
        if (len(key) < lent):
            key = '0'*(lent-len(key)) + key
            return key
        return key

    def generate_subset(self,n):
        return [self.padkeys(bin(i)[2:],3) for i in range(2**n)]


atk = Attack([6,5,1,0,3,2,7,4],delta_h)
p_c = [(('000110','000111'),('110110','110010')),
        (('001000','001001'),('001101','000011')),
        (('001100','001101'),('111001','100000')),
        (('011000','011001'),('011101','011111')),
        (('011010','011011'),('101001','101000')),
        (('100110','100111'),('111110','100100')),
]

# last3 = atk.attack_last3(*p_c[0])
# print('possible last 3 bits: ',last3)

# first3 = atk.attack_first3(*p_c[1])
# print('possible first 3 bits: ',first3)
last3 = []
first3 = []
for p,c in p_c:
    l3 = atk.attack_last3(p,c)
    f3 = atk.attack_first3(p,c)
    last3.append(l3)
    first3.append(f3)

final_l3 = set(last3[0])
final_f3 = set(first3[0])
for st in last3:
    final_l3 = set.intersection(final_l3,st)
for st in first3:
    final_f3 = set.intersection(final_f3,st)
print('possible last 3 bits: ',final_l3)
print('que5'+'-'*50)
print('possible first 3 bits: ',final_f3)
# p_ar = []
# p1 = ""
# p1_dash = ""
# generate_all("001",p1,p1_dash,p_ar)
# p_array = set(map(lambda x:tuple(sorted(x,key=lambda x:x)),p_ar))
# print(p_array)