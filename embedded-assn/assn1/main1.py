import threading
import time
from threading import Thread,Condition

data = []

def thread1():
    global data
    print("waiting...")
    while not cond.wait():
        daata = [i * 2 for i in data]
        data = [i for i in daata]
        print("all values are doubled")
        time.sleep(3)
        cond2.notify()

def thread2():
    global data
    while 1:
        for i in range(3):
            data.append(i)
        cond.notify()
        print('waiting for thread1 to complete the work')
        cond2.wait()
        print(data)
        

cond = Condition()
cond2 = Condition()

t1 = Thread(target = thread1)
t2 = Thread(target = thread2)

t1.start()
t2.start()

t1.join()
t2.join()

