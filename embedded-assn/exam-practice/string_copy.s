		area mydata, DATA, readonly
string 	DCB "this is nirbhay sharma",0
lenstr  DCD 21
	
		area targetdata, DATA
tarstr	DCB ""

		area mycode, CODE, READONLY
		export __main
			
__main	PROC
		
		ldr r0, =string
		ldr r1, =tarstr
		LDR r2, =lenstr
		ldr r2, [r2]
		
		mov r3, #0 ; counter
loop 	cmp r3, r2
		bgt stop
		
		ldrb r4, [r0, r3]
		strb r4, [r1,r3]
		add r3, r3, #1
		B loop
		endp
stop 	B stop
		end