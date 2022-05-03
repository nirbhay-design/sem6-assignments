flags = -O3 -march=native -fopenmp

all: fea ff3

lib:
	gcc -c -std=c99 -O3 -march=native common/FEA_Library/block_enc/*.c
	gcc -c -std=c99 -O3 -march=native common/FEA_Library/transform_naive/*.c
	ar crv libfea.a *.o
	rm fea_enc.o
	rm fea_interface.o
	rm math_simple.o
	rm transform_naive.o

fea: lib
	g++ $(flags) FEA1_Linear.cpp libfea.a -o FEA1_Linear
	g++ $(flags) FEA1_MsgRecovery.cpp libfea.a -o FEA1_MsgRecovery
	g++ $(flags) FEA1_ChiSq.cpp libfea.a -o FEA1_ChiSq
	g++ $(flags) FEA2_Linear.cpp libfea.a -o FEA2_Linear
	g++ $(flags) FEA2_ChiSq.cpp libfea.a -o FEA2_ChiSq

ff3:
	g++ $(flags) FF3_Linear.cpp -o FF3_Linear -lcrypto
	g++ $(flags) FF3_ChiSq.cpp -o FF3_ChiSq -lcrypto
	g++ $(flags) FF3_MsgRecovery.cpp -o FF3_MsgRecovery -lcrypto
	g++ $(flags) FF3_MsgRecoveryRight.cpp -o FF3_MsgRecoveryRight -lcrypto
	g++ $(flags) FF3_Test.cpp -o FF3_Test -lcrypto

clean:
	rm -f FEA1_Linear FEA1_ChiSq FEA1_MsgRecovery
	rm -f FEA2_Linear FEA2_ChiSq
	rm -f FF3_Linear FF3_ChiSq FF3_MsgRecovery FF3_MsgRecoveryRight FF3_Test
	rm -f libfea.a
