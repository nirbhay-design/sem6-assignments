#ifndef FF3_DISTINGUISHERS_H_INCLUDE_GUARD
#define FF3_DISTINGUISHERS_H_INCLUDE_GUARD

#include "common/ff3.h"
#include <complex>
#include <cmath>
#include <vector>
#include <iostream>

std::complex<double> FF3_fixedInputLinearDistinguisher(FF3& cipher, u64 mask, size_t SampSize)
{
    u8 tweak[8] = { 0 };
    fillRandom_fillZero(tweak + 4, 4, cipher.gen); // T_L is fixed

    std::complex<double> c (0, 0);

    std::vector<u8> input(2 * cipher.input_size);
    std::vector<u8> output(2 * cipher.input_size);
    
    // Generate a random fixed right input
    std::uniform_int_distribution<> distribution(0, cipher.domain_size - 1);
    u64_to_bytes(distribution(cipher.gen), cipher.input_size, input.data() + cipher.input_size);
    
    for (size_t i = 0; i < SampSize; ++i) {
        // Generate a random left input
        u64_to_bytes(distribution(cipher.gen), cipher.input_size, input.data());
        fillRandom_fillZero(tweak, 4, cipher.gen); // T_R is random
        cipher.encrypt(output.data(), input.data(), tweak);
        
        const int64_t x = bytes_to_uint<u64>(input.data(),  cipher.input_size);
        const int64_t y = bytes_to_uint<u64>(output.data(), cipher.input_size);
        
        const u64 z = mask * (y > x ? y - x : y - x + cipher.domain_size) % cipher.domain_size;
        std::complex<double> power(0, 2 * M_PI * z / cipher.domain_size);
        c += exp(power);
    }
    return (c / (double)SampSize);
}

std::vector<double> FF3_fixedInputPrDistribution(FF3& cipher, u8* tweak, u64 SampSize, u8* input)
{
    std::vector<double> PrD(cipher.domain_size, 0);
    
    std::uniform_int_distribution<> distribution(0, cipher.domain_size - 1);
    std::vector<u8> output(2 * cipher.input_size);

    for (size_t i = 0; i < SampSize; ++i) {
        fillRandom_fillZero(tweak, 4, cipher.gen);
        cipher.encrypt(output.data(), input, tweak);
        const u64 x = bytes_to_uint<u64>(output.data(), cipher.input_size);
        PrD[x] += 1;
    }
    return PrD;
}

std::vector<double> FF3_PrDistribution(FF3& cipher, u8* tweak, u64 SampSize, u8* right_input)
{
    std::uniform_int_distribution<> distribution(0, cipher.domain_size - 1);

    std::vector<u8> input(2 * cipher.input_size);
    std::vector<u8> output(2 * cipher.input_size);
    std::copy(right_input, right_input + cipher.input_size, input.begin() + cipher.input_size);

    std::vector<double> PrD(cipher.domain_size, 0);
    for (size_t i = 0; i < SampSize; ++i) {
        // Randomize left side of input
        u64_to_bytes(distribution(cipher.gen), cipher.input_size, input.data());
        fillRandom_fillZero(tweak, 4, cipher.gen);
        cipher.encrypt(output.data(), input.data(), tweak);
        const int64_t x = bytes_to_uint<u64>(input.data(),  cipher.input_size);
        const int64_t y = bytes_to_uint<u64>(output.data(), cipher.input_size);
        const u64 z = (y > x ? y - x : y - x + cipher.domain_size) % cipher.domain_size;

        PrD[z] += 1;
    }
    return PrD;
}

double FF3_chiSqDistinguisher(FF3& cipher, u64 mask, size_t SampSize)
{
    u8 tweak[8] = { 0 };
    fillRandom_fillZero(tweak + 4, 4, cipher.gen); // T_L is fixed
    
    std::uniform_int_distribution<> distribution(0, cipher.domain_size - 1);
    std::vector<u8> right_input(cipher.input_size);
    // Generate a random fixed right input
    u64_to_bytes(distribution(cipher.gen), cipher.input_size, right_input.data());
    
    std::vector<double> histogram = FF3_PrDistribution(
        cipher, tweak, SampSize, right_input.data()
    );
    //std::vector<double> histogram(cipher.domain_size, 0);
    //for (size_t i = 0; i < SampSize; ++i) {
    //    // Generate a random left input
    //    u64_to_bytes(distribution(cipher.gen), cipher.input_size, input.data());
    //    fillRandom_fillZero(tweak, 4, cipher.gen);
    //    cipher.encrypt(output.data(), input.data(), tweak);
    //    
    //    const int64_t x = bytes_to_uint<u64>(input.data(),  cipher.input_size);
    //    const int64_t y = bytes_to_uint<u64>(output.data(), cipher.input_size);
    //    const u64 z = (y > x ? y - x : y - x + cipher.domain_size) % cipher.domain_size;
    //    histogram[z] += 1;
    //}
     
    const double expected_count = SampSize / cipher.domain_size;
    double sum = 0;
    for(double x : histogram)
        sum += std::pow(x - expected_count, 2) / expected_count;
    return sum;
}

#endif
