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

	RCC->AHB1ENR = 0X40; // ENABLING CLOCK FOR PORT G
	GPIOG->MODER = 0X5000000;
	GPIOG->ODR = (1<<13) | (1<<14);
	while (1) {
		GPIOG->ODR = 0X0;
		delay(100);
		GPIOG->ODR = (1<<13) | (1<<14);
		delay(100);
	}

}