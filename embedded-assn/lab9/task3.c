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

	RCC->AHB1ENR = 0X41; // ENABLING CLOCK FOR PORT G & A
	GPIOG->MODER = 0X1000000;
	GPIOA->MODER = 0x0;
	
	while (1) {
		if (GPIOA->IDR & 0X01) {
			GPIOG->ODR = (1<<13);
			while (GPIOA->IDR & 0X01) {
				;
			}
		}
		GPIOA->ODR = 0X0;
		
	}

}