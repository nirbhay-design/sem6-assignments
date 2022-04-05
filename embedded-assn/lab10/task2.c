#include "stm32f4xx.h"
void delay(int dd){
	for (int i = 0;i<dd;i++){
		for (int j = 0;j<300000;j++){
			;
		}
	}
}

main(void)
{
    // enabline clocks
	RCC->AHB1ENR = 0X10; // ENABLING CLOCK FOR PORT E
    RCC->APB2ENR = 0X01; // ENABLINE TIM1

    // configuring pin (PE8)
    GPIOE->MODER = 0X20000;
    GPIOE->PUPDR = 0X00;

    // configuring timer
    TIM1->CR1 = 0X01;
    

}