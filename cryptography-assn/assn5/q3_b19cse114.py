import random, json, os

def modulo_exponentiation(bas,exp,N):
    if (exp == 0):
        return 1;
    if (exp == 1):
        return bas % N;
    t = modulo_exponentiation(bas, exp // 2,N);
    t = (t * t) % N;
    if (exp % 2 == 0):
        return t;
    else:
        return ((bas % N) * t) % N;

def square_multiply(bas,exp):
    if (exp == 0): return 1;
    if (exp == 1): return bas;
    if (exp & 1):
        return bas * square_multiply(bas * bas, (exp-1)//2)
    else:
        return square_multiply(bas * bas,exp//2)

def write_to_file(filename,dictionary):
    with open(filename, 'a') as f:
        f.write(str(dictionary) + "\n")

def find_generator(prime_p):
    while True:
        random_a = random.randint(2,prime_p-1)
        rem = modulo_exponentiation(random_a,prime_p-1,prime_p)
        if (rem == 1): return random_a;


class Prime_generator_machine(object):
    def __init__(self,bits_in_prime):
        self.bip = bits_in_prime;
    
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

    def generate_random_bits(self):
        return int("1"+ ''.join([random.choice(["0","1"]) for _ in range(self.bip-2)])  + "1",2)

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
            final_prime = self.generate_random_bits()
            a = self._check_prime(final_prime)
        # print(iterations)
        return final_prime;


pgm = Prime_generator_machine(511)

def generate_sophie_germain_prime(pgm,thresh):
    sgp = None;
    iterations = 0;
    p_dash = 0
    while True:
        p_dash = pgm.generate_prime()

        # print(f'p_dash prime_test: {pgm._check_prime(p_dash)}')
        iterations += 1
        print(f'iterations: {iterations}',end='\r')
        sophie_germain_prime = 2*p_dash + 1
        if (pgm._check_prime(sophie_germain_prime)):
            sgp = sophie_germain_prime
            break;
        if (iterations == thresh): 
            break;
        # print(f'sophie germain prime test: {pgm._check_prime(sophie_germain_prime)}')

        # print('p_dash:',p_dash)
        # print('generated sophie germain prime:',sophie_germain_prime)
    print('p_dash:',p_dash)
    return ((sgp,iterations) if sgp is not None else ("None",iterations));




sophie_germain_prime,iterations = generate_sophie_germain_prime(pgm,200)
print('sphie_germain_prime: ',sophie_germain_prime)
write_to_file('sophie-germain-prime.txt',{"iter":iterations,"sgp":sophie_germain_prime})
if sophie_germain_prime == "None":
    print('cannot find sophie germain prime till 200 iterations !!! Try running again')
    exit(0)
generator = find_generator(sophie_germain_prime)
# for a prime order group every element is a generator
print('found generator: ',generator)

exit(0)

class Alice(object):
    def __init__(self,g):
        self.a = random.randint(3,10)
        self.g = g
    
    def _generate_key(self):
        return square_multiply(self.g,self.a)

    def _generate_final_key(self,bob_g_random):
        return square_multiply(bob_g_random,self.a)

class Bob(object):
    def __init__(self,g):
        self.b = random.randint(3,10)
        self.g = g
    
    def _generate_key(self):
        return square_multiply(self.g,self.b)

    def _generate_final_key(self,alice_g_random):
        return square_multiply(alice_g_random,self.b)

def diffie_hilmann_exchange(g):
    alice = Alice(g)
    bob = Bob(g)

    alice_generated_key = alice._generate_key()
    bob_generated_key = bob._generate_key()

    final_key_at_alice = alice._generate_final_key(bob_generated_key)
    final_key_at_bob = bob._generate_final_key(alice_generated_key)

    print(final_key_at_alice,final_key_at_bob)
    print(final_key_at_alice==final_key_at_bob)
    

diffie_hilmann_exchange(23)


