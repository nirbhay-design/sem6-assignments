#include "stm32f4xx.h"
main(void)
{
int x,y;
x=0x1B;
RCC->AHB1ENR |=1; // Enables Clock

if (x >= 0 && x < 100) {
GPIOB->MODER = 0X15555;
GPIOB->ODR = 0X000;
y = 2 * x  + 2;
GPIOB->ODR = y;
}

if (x >= 100 && x < 200){
GPIOC->MODER = 0X55555555;
GPIOC->ODR = 0X0000;
y = x * x - 2 * x;
GPIOC->ODR = y;
}

if (x >= 200 && x < 256){
GPIOD->MODER = 0X5555;
GPIOD->ODR = 0X00;
y = x - 150;
GPIOD->ODR = y;
}


}