def extended_eucledian(a,b):
    if (a%b == 0): return (b,0,1)
    val = [[a,1,1,0],[b,a//b,0,1]]
    while val[-1][0] != 1:
        new_val = []
        new_val.append(val[-2][0] % val[-1][0])
        if (new_val[0] == 0): return (val[-1][0],val[-1][-2],val[-1][-1])
        new_val.append(val[-1][0] // new_val[0])
        new_val.append(val[-2][-2] - val[-1][1] * val[-1][-2])
        new_val.append(val[-2][-1] - val[-1][1] * val[-1][-1])
        val.append(new_val)  
    return (val[-2][1],val[-1][-2],val[-1][-1]);

class rsa_algorithm(object):
    def __init__(self):
        self.p = 10888869450418352160768000001
        self.q = 265252859812191058636308479999999
        self.phi_n = (self.p-1)*(self.q-1)
        self.n = self.p * self.q
    def find_e(self):
        for i in range(3,100,2):
            gcd,x,y = extended_eucledian(self.phi_n,i)
            if (gcd == 1):
                return (i,y)

    def rsa_encryption(self,msg):
        self.e,self.__d = self.find_e();
        encoded_string = []
        encoded_msg = bytes(msg,'utf-8')
        for char in encoded_msg:
            encoded_string.append(self.modulo_exponentiation(char,self.e,self.n))        
        return ''.join(map(lambda x: bytearray(hex(x),'utf-8').decode() + ' ' ,encoded_string))[:-1]

    def rsa_decryption(self,cipher):
        decoded_msg = []
        for i in cipher.split(' '):
            cipher_msg = i.strip();
            cipher_msg = int(cipher_msg.encode(),16)
            decoded_msg.append(self.modulo_exponentiation(cipher_msg,self.__d,self.n))
        return ''.join(map(lambda x:chr(x),decoded_msg))


    def square_multiply(self,bas,exp):
        if (exp == 0): return 1;
        if (exp == 1): return bas;
        if (exp & 1):
            return bas * self.square_multiply(bas * bas, (exp-1)//2)
        else:
            return self.square_multiply(bas * bas,exp//2)

    def modulo_exponentiation(self,bas,exp,N):
        if (exp == 0):
            return 1;
        if (exp == 1):
            return bas % N;
        t = self.modulo_exponentiation(bas, exp // 2,N);
        t = (t * t) % N;
        if (exp % 2 == 0):
            return t;
        else:
            return ((bas % N) * t) % N;


original_text = "Nirbhay Sharma is a good boy !!!";
rsa = rsa_algorithm();
enc = rsa.rsa_encryption(original_text);



print('public n: ',rsa.n)
print('public e:',rsa.e)

print('#'*25 + ' original_text ' + '#'*25)
print(original_text)

print('#'*25 + ' encrypted text ' + '#'*25)
print(enc)

dec = rsa.rsa_decryption(enc)
print('#'*25 + ' decrypted text ' + '#'*25)
print(dec)
