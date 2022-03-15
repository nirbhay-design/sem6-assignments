## Nirbhay Sharma (B19CSE114)
## Digital Systems Lab - 4 

---

### QUE - 1

```arm
	AREA CONDITIONALS , CODE , READONLY
	EXPORT __main
		
__main
	MOV R0,#5000
	MOV R1,#1
	CMP R0,#10
	BLE STORE9N
	CMP R0,#100
	BLE STORE8N
	CMP R0,#1000
	BLE STORE7N
	B STORE6N
	
	
STORE9N
	MOV R2,#9
	MUL R1,R0,R2
	B STOP
	
STORE8N
	MOV R2,#8
	MUL R1,R0,R2
	B STOP
	
STORE7N
	MOV R2,#7
	MUL R1,R0,R2
	B STOP

STORE6N
	MOV R2,#6
	MUL R1,R0,R2
	B STOP
	
STOP B STOP
	END
```

**logic** - applied various if else conditions using CMP instruction and accordingly updated the registers, register R0 stores the value N, register R1 stores the final result and R2 stores the multiplicative factor by which the register R0 is multiplied

|N = 5|N = 50|N = 500|N=5000|
|---|---|---|---|
|![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/embed-lab4/1.PNG?raw=true)|![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/embed-lab4/2.PNG?raw=true)|![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/embed-lab4/3.PNG?raw=true)|![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/embed-lab4/4.PNG?raw=true)|
|R1=0x2D=45|R1=0x190=400|R1=0xDAC=3500|R1=0x7530=30000|


### QUE - 2

```arm
	AREA CONDITIONALS , CODE , READONLY
	EXPORT __main
		
__main
	MOV R0,#50
	CMP R0,#0
	BEQ STORE128
		
	AND R2,R0,#1
	CMP R2,#0
	BEQ STORE256
	B STORE512
	
STORE128
	MOV R1,#128
	B STOP
	
STORE256
	MOV R1,#256
	B STOP
	
STORE512
	MOV R1,#512
	B STOP
	
STOP B STOP
	END
```
**logic** - applied various if else conditions using CMP instruction and accordingly updated the registers, register R0 stores the value N, register R1 stores the final result and R2 stores the modulo of R0 with 2 (R0 % 2)

|N = 0|N = 23|N = 50|
|---|---|---|
|![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/embed-lab4/5.PNG?raw=true)|![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/embed-lab4/6.PNG?raw=true)|![img](https://github.com/nirbhay-design/markdown-images-pdf-repo/blob/master/embed-lab4/7.PNG?raw=true)|
|R1=0x80=128|R1=0x200=512|R1=0x100=256|