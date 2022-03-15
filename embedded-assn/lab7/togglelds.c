#include "stm32f407xx.h"
void delay(int dd);
int main()
{
RCC->AHB1ENR |=1; // Enables Clock
GPIOA->MODER |=0x5000; // Mode Register
GPIOA->ODR=0xc0; // Output Data Register
while(1)
{
GPIOA->ODR=0x00;
delay(1200);
GPIOA->ODR=0xc0;
delay(1200);
}
// return 1;
}
void delay (int dd) //Delay function definition
{
int i;
for (;dd>0;dd--)
{
for(i=0;i<30000;i++);
}
}