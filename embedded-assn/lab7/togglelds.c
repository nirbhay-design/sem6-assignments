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
	TIM1->CCER = (1 << 2);
	
	TIM1->CR1 |= 0X01;

    int tim_values_terms = 7; 
    int tim_values[] = {200, 300, 500, 400, 900, 800, 600};
    
    for (int i = 0;i<tim_values_terms;i++){
	    TIM1->CCR1 = tim_values[i];
    } 

}