#include "stm32f4xx.h"
main(void)
{
    int delay_value = 10;
    SysTick->LOAD = 16000000-1;
    SysTick->VAL = 0;
    for (int i = 0;i<delay_value;i++) {
        SysTick->CTRL = 0x05;
        while (! (SysTick->CTRL & 0x10000) );
    }
}


#include "stm32f4xx.h"
main(void)
{
    RCC->AHB1ENR = 0X01;
    GPIOA->MODER = 0X5000;
    GPIOA->ODR = 0XC0;
    SysTick->LOAD = 16000000-1;
    SysTick->VAL = 0;
    SysTick->CTRL = 0x07;
    while (1){
        if (SysTick->CTRL & 0x10000){
                GPIOA->ODR ^= 0xc0;
        }
    }
    
}