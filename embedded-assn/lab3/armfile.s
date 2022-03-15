	AREA mydata, DATA, READONLY
data1 DCD 7
	AREA mydata1, DATA
data2 DCD 0
	AREA value, CODE
    EXPORT __main
__main 
    LDR r3,=data1
    LDR r0,[r3]
    ;mov r0, #2
	ADD r0,r0,#3
	LDR r1,=data2
	STR r0,[r1]
	
	LDR r3,=data2
    ;MOV r1,#3
    ;MUL r0, r0,r1
	
    ;mul r0,r0,r1
    ;mul r0,r0,r1
stop B stop	
	END
	