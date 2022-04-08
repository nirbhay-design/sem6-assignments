import random
import math
rr=random.SystemRandom()
def power(x,y,p):
    y=int(y)
    ans=1
    x%=p
    while(y>0):
        if(y&1):
            ans=(ans*x)%p
        y=int(y/2)
        x=(x*x)%p
    return ans

def EEA(a,b):
    if(b==0):
        x=1
        y=0
        return [a,x,y]
    
    d=EEA(b,a%b)
    gcd=d[0]
    x1=d[1]
    y1=d[2]
    x=y1
    y=x1-(y1*math.floor(a/b))
    return [gcd,x,y]



def check(n,r):
    p=n-1
    while(p%2==0):
        p/=2
        
    
    x=pow(r,int(p),int(n))
    if(x==1):
        return 0
    while(p<n-1):
        if(pow(int(r),int(p),int(n))==n-1):
            return 0
        p*=2
    return 1
        
            
    
    
def miller_rabin(n,k):
    if(n%5==0):
        return 0
    
    if(n==3 or n==2):
        return 1
    if(n<=4):
        return 0
    if(n%2==0):
        return 0
    for i in range(k):
        r=rr.randrange(2,n-1)
        if(check(n,r)):
            return 0
    return 1
    
    
    
def gen_num(k):
    p=1
    n=random.randint((1<<k)+1, (1<<(k+1))-1)
    
    return n
   
    
def gen_prime(k):
    
    n=gen_num(k)
    while(miller_rabin(n, 40)==0):
        #print(n)
        n=gen_num(k)
        #print(n)
        
    return n

def gen(k):
    for i in range(1<<k,1<<(k+1)):
        if(miller_rabin(i,40)==1):
            return i
    
    
# p=gen_prime(100)
# print(p)
# q=gen_prime(100)
# print(q)
# n=p*q
# print(f'p={p}')
# print(f'q={q}')
# d=EEA(p, q)
# print(d)

# print(f'n={n}')



