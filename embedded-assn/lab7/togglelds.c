#include "stm32f4xx.h"
main(void)
{
		RCC->AHB1ENR = 0x01;
		GPIOA->MODER = 0X04;
		GPIOA->ODR = 0XC0;
	
		RCC->APB1ENR = 0X01;
		TIM2->PSC = 1599;
		TIM2->ARR = 999;
		TIM2->CNT = 0;
		TIM2->CR1 = 0X01;
	
		while (1) {
			while (!(TIM2->SR & 1)) {
				TIM2->SR = 0;
				GPIOA->ODR ^= 0XC0;
			}
		}
		
	
}

    