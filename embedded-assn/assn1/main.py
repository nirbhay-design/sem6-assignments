import threading
from time import sleep

e1 = threading.Event()
e2 = threading.Event()

int_isr_vec = []

isr = {0:'The error is now gone',1:'error is resolved',2:'issue is solved'}

def checkdevices():
    while True:
        while not e1.is_set():
            print('waiting for the device interrupt')
            sleep(0.5)
        e1.wait()
        while e1.is_set():
            e2.set()
            print('sending the requested isr_vector to microprocessor')
            e2.clear()
            sleep(5)

def handleint():
    while (True):
        while (not e2.is_set()):
            print("current program is executing")
            sleep(0.5)
        e2.wait()
        while (e2.is_set()):
            if (len(int_isr_vec) != 0):
                while (len(int_isr_vec) != 0):
                    vector = int_isr_vec.pop(0)
                    print(isr[vector])
                    print(f'interrupt handled for {vector}')
                    sleep(0.2)
                sleep(1)
        




def generateint(i):
    while 1:
    
        sleep(3)
        e1.set()
        print(f"interrupt generated from device {i}")
        int_isr_vec.append(i);
        sleep(2)
        e1.clear()
        sleep(5)


prioarbiter = threading.Thread(target = checkdevices)
microprocessor = threading.Thread(target = handleint)

prioarbiter.start()
microprocessor.start()

devices = []
for i in range(3):
    d1 = threading.Thread(target = generateint,args=[i])
    d1.start()
    devices.append(d1)

for device in devices:
    device.join()

prioarbiter.join()
microprocessor.join()



# thrd1.join()
# thrd2.join()

