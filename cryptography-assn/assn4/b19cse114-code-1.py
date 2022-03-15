'''
NIRBHAY SHARMA (B19CSE114)
'''

from Crypto.Cipher import AES
import random

# file = AES.new()
ivdomain = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
class AES_encryption_decryption(object):
    def __init__(self):
        self.key = "cryptographycour".encode('utf-8')
        self.iv = ''.join([random.choice(ivdomain) for _ in range(16)]).encode('utf-8')
        print('aes_iv:',self.iv)
    def encrypt(self,pt):
        aes_algo = AES.new(self.key,AES.MODE_CBC,self.iv)
        messages = self.padding(pt)
        print('padded_message:',messages)
        ciphertext = aes_algo.encrypt(messages)
        return (self.iv,ciphertext)

    def decrypt(self,ct):
        aes_algo = AES.new(self.key,AES.MODE_CBC,self.iv)
        plaintext = aes_algo.decrypt(ct)
        return plaintext

    def oracle(self,ct,iv):
        aes_algo = AES.new(self.key,AES.MODE_CBC,iv)
        plaintext = aes_algo.decrypt(ct)
        pt = plaintext
        print(pt)
        last_value = pt[-1]
        if(last_value >= 16):
            return False
        repeat_length = 0
        for i in range(len(pt)-1,0,-1):
            if (pt[i] == last_value):
                repeat_length += 1
            else:
                break
        if (repeat_length == last_value):
            return True
        return False
            

    def padding(self,x):
        next_mult16 = len(x)
        while (next_mult16%16 != 0):
            next_mult16 += 1
        pad_value = next_mult16-len(x)        
        return (x.encode('utf-8') + bytearray([pad_value for _ in range(pad_value)]))

PLAIN_TEXT = "b19cse114_nirbhaysharma_yogendrasharma_archanasharma_meerut"
# print(len(PLAIN_TEXT))
# print(PLAIN_TEXT.encode('ascii'))

aes = AES_encryption_decryption()
ivv,ct = aes.encrypt(PLAIN_TEXT)
print('cipher text: ',ct)
pt = aes.decrypt(ct)
print('decrypted text: ',pt.decode())
# print(len(pt))

iv = ''.join([random.choice(ivdomain) for _ in range(16)]).encode('utf-8')
print('random_iv:',iv)
print(aes.oracle(ct,iv))

# print(aes.padding_divide(PLAIN_TEXT))
# print(aes.iv)
# print(aes.xor_bytes('123'.encode('utf-8'),'abc'.encode('utf-8')))
