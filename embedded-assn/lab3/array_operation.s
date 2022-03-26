MAIN   LDR     R1, =LABEL
       MOV     R2,#0
       MOV     R3 , #0
LOOP   CMP     R2 , #4
       BGT     STOP
       LDR     R4, [R1]
       ADD     R3, R3, R4
       ADD     R1 , R1,#4
       ADD     R2,R2,#1
       B       LOOP
STOP   END

LABEL  DCD     1,2,3,4,5


	AREA mydatas, DATA
data1 space 40
a DCD 1,2,3,4,5,6,7,8,9,10
	
	area spaceuse, code
	export __main

__main 
	LDR r0, =data1
	LDR r1, =a

	MOV r2, #0
	MOV r3, #0
	
	;ldr r1, =a
	
	ldr r5, [r1]
	ldr r6,[r1 , #8]
	ldr r7 ,[r1, #20]
	end
loop 
	cmp r2,#9
	bgt checkcopy
	LDR r4, [r1]
	str r4,[r0]
	ADD r0, r0, #4
	ADD r1, r1, #4
	ADD r2, r2 ,#1
	B loop
	
checkcopy
	ldr r1, =a
	
	ldr r5, [r1]
	ldr r6,[r1 , #8]
	ldr r7 ,[r1, #20]
	
	b stop
stop B stop
	end
       
		

	AREA mydatas, DATA
LABEL DCD 1,2,3,4,5
	
	area spaceuse, code
	export __main

__main 	
	LDR     R1, =LABEL
	MOV     R2,#0
	MOV     R3 , #0
LOOP   
	CMP     R2 , #4
	BGT     stop
	LDR     R4, [R1]
	ADD     R3, R3, R4
	ADD     R1 , R1,#4
	ADD     R2,R2,#1
	B       LOOP

stop B stop
	end