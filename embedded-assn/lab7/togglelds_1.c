#include "stm32f4xx.h"
main(void)
{
unsigned int x,y,z,w;
x=0x1B;
y=0x0B;
z=0x1C;
RCC->AHB1ENR |=1; // Enables Clock
GPIOE->MODER |=0x55555555; // Mode Register
GPIOE->ODR=0x0000; // Output Data Register
w=x+y*z;
GPIOE->ODR=w; // w value at output Data Register
}