import math
import time

class processor(object):
    def __init__(self):
        self.inta = 0

    def ackint(self):
        self.inta = 1

class prioarbiter(object):
    def __init__(self):
        self.int = 0
        self.inta = 0

    def generateint(self):
        self.int= 1

    def recinta(self,devicelist,a):
        self.inta = 1
        b = list(sorted(a,key=lambda x:x))
        devicelist[b[-1]].getack();

        return b[-1]
    
class peripheraldevice(object):
    def __init__(self,priority,intvec):
        self.priority = priority
        self.intvecaddr = intvec
        self.ireq = 0
        self.iack = 0

    def assertreq(self):
        self.ireq = 1
    
    def getack(self):
        self.iack = 1
        
# prioarbiter: list of devices, inta, intack

class hardware(object):
    def __init__(self):
        self.devicelist = []
        self.systembus= 0
        self.processor = processor()
        self.parbiter = prioarbiter()
        self.pc = 10
        self.isr = {}

    def run(self):
        nod = int(input('enter number of devices you want to connect at peripheral: '))
        for i in range(nod):
            self._insert()

        while 1:
            time.sleep(0.5)
            print('enter 1 for generating interrupt from peripheral devices')
            print('enter 3 to exit')
            a = int(input())
            if (a == 3):
                exit()

            elif (a == 1):
                self._generateInt()

    def _insert(self):
        addr = "0x"+str(self.pc)
        device = peripheraldevice(len(self.devicelist),addr)
        self.pc += 4
        self.isr[addr] = f"executing routine at isr location {addr} for handling interrupt for device {len(self.devicelist)}"
        self.devicelist.append(device)
        print(f'new device successfully connected with id: {len(self.devicelist)-1}')

    def _generateInt(self):
        print('available devices:')
        for idx,j in enumerate(self.devicelist):
            print(f'device {idx}')
        a = list(map(int,input('enter the devices id (space separated) which generates the interrupt: ').strip().split()))
        for i in a:
            if (i >= len(self.devicelist)):
                print(f'device doesnot exist with id {i}')
                exit()
            print(f'request asserted for device {i}')
            self.devicelist[i].assertreq()
        if (self.devicelist.__len__() > 0):
            try:
                self.parbiter.generateint()
            except Exception as e:
                print('int cannot be generated')

            if (self.parbiter.int == 1):
                self.processor.ackint()
            deviceno = self.parbiter.recinta(self.devicelist,a)
            self.systembus = self.devicelist[deviceno].intvecaddr
            print(f'{self.isr[self.systembus]}') 
            self._reset_all_buses()

    def _reset_all_buses(self):
        self.parbiter.int = 0
        self.parbiter.inta = 0
        self.processor.inta = 0
        for i in range(len(self.devicelist)):
            self.devicelist[i].ireq = 0
            self.devicelist[i].iack = 0
        self.systembus = 0




hdware = hardware()
hdware.run() 

