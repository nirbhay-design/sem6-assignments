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
	GPIOG->MODER = 0X4000000;
	GPIOA->MODER = 0x0;
	int againon = 0;
	while (1) {
		if (GPIOA->IDR & 0X01) {
			againon = 1-againon;
			if (againon == 1){
				GPIOG->ODR = (1<<13);
			} else {
				GPIOG->ODR = 0x0;
			}
			while (GPIOA->IDR & 0X01);
		}
	}

}
