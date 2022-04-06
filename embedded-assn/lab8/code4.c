#include "stm32f4xx.h"
main(void)
{

	RCC->APB2ENR |= 0X100;
	RCC->AHB1ENR |= 0X01;
	
	ADC1->CR2 |= 0X0402; // ENABLING 10TH AND 2ND BIT OF ADC1 REGISTER
	GPIOA->MODER |= 0X03; // ADC MODE
	
	while (1) {
		ADC1->CR2 |= 0X01;
		ADC1->SQR3 |= 0;
		ADC1->SR = 0;
		ADC1->CR2 |= (1<<30);
		while (!(ADC1->SR & (1<<1)));
		
	}
	

}