import random
import sys
sys.setrecursionlimit(1030)

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
        # self.p = 10888869450418352160768000001
        # self.q = 265252859812191058636308479999999
        self.p = self.generate_prime();
        self.q = self.generate_prime();
        # self.p = 155;
        # self.q = 21711;
        print('P: ',self.p)
        print('Q: ',self.q)
        self.phi_n = (self.p-1)*(self.q-1)
        self.n = self.p * self.q
    def find_e(self):
        for i in range(3,100,2):
            gcd,x,y = extended_eucledian(self.phi_n,i)
            if (gcd == 1):
                return (i,y)

    def rsa_encryption(self,msg):
        self.e,self.__d = self.find_e();
        # print('inside d:',self.__d)
        if (self.__d < 0):
            print('d < 0, making it positive !!!')
            self.__d = self.phi_n + self.__d
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
            # print(f'cipher msg: {cipher_msg}')
            decoded_msg.append(self.modulo_exponentiation(cipher_msg,self.__d,self.n))
        # print(decoded_msg)
        # return 
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

    def generate_random_512(self):
        return int("1"+ ''.join([random.choice(["0","1"]) for _ in range(510)])  + "1",2)

    def find_s_t(self,num):
        new_num = num - 1;
        s = 0;
        while (new_num & 1 == 0):
            s += 1;
            new_num >>= 1;
        return (s,new_num)

    def miller_rabin_test(self,num,s,t):
        new_num = num - 1;
        aa = random.randint(2,new_num)
        b_i = self.modulo_exponentiation(aa,t,num);
        if (b_i == 1 or b_i == num - 1):
            return 1;
        pow_2 = 0;
        while (True):
            pow_2 += 1
            if (pow_2 == s+1):
                break;
            b_i = self.modulo_exponentiation(b_i,2,num);
            # if (b_i == 1): return 0;
            if (b_i == num - 1): return 1;
        return 0;

    def _check_prime(self,num):
        s,t = self.find_s_t(num);
        for i in range(100):
            vote = self.miller_rabin_test(num,s,t)
            if (vote == 0):
                return False;
        return True;


    def generate_prime(self):
        a = False;
        final_prime = None;
        # iterations = 0;
        while (not a):
            # iterations+=1
            final_prime = self.generate_random_512()
            a = self._check_prime(final_prime)
        # print(iterations)
        return final_prime;

    def fast_modulo_exponentiation(self,base,power,N):
        dp = [-1]

            

        

    

original_text = "Nirbhay Sharma is a good boy !!! and he studies at IIT Jodhpur and he likes to do exercise and yoga";
rsa = rsa_algorithm();

# print(rsa.generate_prime())
# print(rsa.generate_prime())
# exit(0)

enc = rsa.rsa_encryption(original_text);

print('private d:',rsa._rsa_algorithm__d)
print('public n: ',rsa.n)
print('public e:',rsa.e)

print('#'*25 + ' original_text ' + '#'*25)
print(original_text)

print('#'*25 + ' encrypted text ' + '#'*25)
print(enc)

dec = rsa.rsa_decryption(enc)
print('#'*25 + ' decrypted text ' + '#'*25)
print(dec)

