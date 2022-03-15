	area sumn, code
	export __main
__main  
	MOV     R0,#10

	MOV	R1,#0
	MOV     R2, #0
LOOP  
	CMP     R1, R0
	BGT     stop
	ADD     R2,R2,R1
	ADD     R1,R1,#1
	B       LOOP
stop  B stop
	  end
