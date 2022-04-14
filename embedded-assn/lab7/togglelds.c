#include "stm32f4xx.h"

main(void)
{
  // enabline clocks
	RCC->AHB1ENR = 0X10; // ENABLING CLOCK FOR PORT E
	RCC->APB2ENR = 0X01; // ENABLINE TIM1

	// configuring pin (PE8)
	GPIOE->MODER = 0X20000;
	GPIOE->PUPDR = 0X00;
	GPIOE->AFR[1] = 0X01;

	// configuring timer
	TIM1->CR1 = 0X01;
	TIM1->PSC = 15;
	TIM1->ARR = 999;
	TIM1->CCMR1 = 0X68;
	TIM1->CR1 |= (1 << 7);
	TIM1->BDTR = (1 << 15);
	TIM1->CCER = (1 << 10);
	
	TIM1->CCR1 = 500;
	TIM1->CR1 |= 0X01; 

}