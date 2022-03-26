	AREA mydatas, DATA,READONLY
a DCD 1,2,3,4,5,6,7,8,9,10
;data1 space 40
	AREA mydata,DATA
data1 DCD 0,0,0,0,0,0,0,0,0,0
	
	area spaceuse, code,Readonly
	export __main

__main 
	LDR r0, =data1 ; load address of data1
	LDR r1, =a ; load address of a

	MOV r2, #0 ; index
	
	;ldr r1, =a

loop 
	cmp r2,#9 ; comparing with 9 as loop needs to be stopped at that
	bgt checkcopy ; jump to checkcopy to see that array is copied or not
	LDR r4, [r1] ; load first value of array a into r4
	str r4,[r0] ; store r4 value at r0 first location i.e copying first value at of a to data1
	ADD r0, r0, #4 ; increment the address of r0 by 4 to reach next value
	ADD r1, r1, #4 ; similar to above
	ADD r2, r2 ,#1; increment counter 
	B loop ; again loop 
	
checkcopy
	ldr r0, =data1 ; store addr or data1 in r0
	; this for checking that copying is done or not
	ldr r5, [r0]
	ldr r6,[r0 , #8]
	ldr r7 ,[r0, #20]
	
	b stop
stop B stop
	end
       
		