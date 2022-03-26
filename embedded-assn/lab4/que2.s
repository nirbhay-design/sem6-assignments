	AREA CONDITIONALS , CODE , READONLY
	EXPORT __main
		
__main 
	
	MOV R0,#2
	MOV R1,#3
	MOV R2,#4
	
	PUSH {R2,R1,R0}
	POP {R3,R4,R5}
			
STOP B STOP
	END


#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include "stm32f4xx.h"

__asm void your_strcpy(const char *src, char *dst){
	
	loop
		LDRB r2, [r0], #1 
		STRB r2, [r1], #1 
		CMP r2, #0 
		BNE loop 
		BX lr 
}


int main(void){
	const char a[] = "Hello world!";
	char b[20];
	your_strcpy(a, b);
	//your_capitalize(b);
	while (1);
	return 0;
}