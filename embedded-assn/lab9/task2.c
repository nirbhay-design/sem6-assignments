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
	GPIOG->MODER = 0X1000000;
	GPIOG->ODR = (1<<13);
	while (1) {
		GPIOG->ODR = 0X0;
		delay(100);
		GPIOG->ODR = (1<<13);
		delay(100);
	}

}



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
	GPIOG->MODER = 0X4000000;
	GPIOG->ODR = (1<<14);
	while (1) {
		GPIOG->ODR = 0X0;
		delay(100);
		GPIOG->ODR = (1<<14);
		delay(100);
	}

}

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
	int led13=1,led14=0;
	GPIOG->ODR = (1<<13);
	led13--;led14++;
	while (1) {
		if (led14 == 1) {
			GPIOG->ODR = (1<<14);
			led14--;led13++;
			delay(100);
			continue;
		}
		if (led13 == 1) {
			GPIOG->ODR = (1<<13);
			led13--;led14++;
			delay(100);
			continue;
		}
	}

}
