import random

def square_multiply(bas,exp):
    if (exp == 0): return 1;
    if (exp == 1): return bas;
    if (exp & 1):
        return bas * square_multiply(bas * bas, (exp-1)//2)
    else:
        return square_multiply(bas * bas,exp//2)

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


