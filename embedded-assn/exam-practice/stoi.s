		area mydata, DATA, readonly
string 	DCB "12345",0
lenstr  DCD 4
	
		area mycode, CODE, READONLY
		export __main
			
__main	PROC
		
		ldr r0, =string
		LDR r1, =lenstr
		ldr r1, [r1]
		
		mov r2, #0 ; index
		mov r3, #0 ; final_ans
		mov r4, r1 ; pow_of_ten
loop 	cmp r2, r1
		bgt stop
		ldrb r5, [r0,r2]
		add r5, r5, #-48
		mov r6 , #1
		mov r7, #10
		push {r4}
		
loop1	cmp r4, #0
		beq break
		mul r6, r6, r7
		add r4, r4 , #-1
		b loop1
		
break	pop {r4}
		mul r5, r5, r6
		ADD r3, r3, r5
		add r4, r4, #-1
		add r2, r2, #1
		b loop
		
		endp
stop 	B stop
		end
