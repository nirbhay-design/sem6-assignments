		area mydata, DATA, readonly
string 	DCB "101101",0
lenstr  DCD 5
	
		area mycode, CODE, READONLY
		export __main
			
__main	PROC
		
		ldr r0, =string
		LDR r1, =lenstr
		ldr r1, [r1]
		
		mov r2, #0 ; index
		mov r3, r1 ; pow_of_2
		mov r5, #0 ; final ans
		
loop 	cmp r2, r1
		bgt stop
		
		ldrb r4, [r0, r2]
		add r4, r4, #-48
		
		cmp r4, #1
		lsl r4, r4, r3
		addeq r5, r5,r4
		add r3, r3, #-1
		add r2 ,r2, #1
		b loop
		endp
stop 	B stop
		end