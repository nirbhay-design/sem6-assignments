#include "stm32f4xx.h"
main(void)

{
	unsigned short x,y,z;
	x=0x1B;
	y=0x0B;
	RCC->AHB1ENR |=1; // Enables Clock
	GPIOA->MODER |=0x5555; // Mode Register
	GPIOA->ODR=0x00; // Output Data Register
	z=x+y;
	GPIOA->ODR=z; // z value at output Data Register
}