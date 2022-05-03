#include <iostream>
#include <iomanip>

#include "ff3_distinguishers.h"

std::vector<size_t> FF3_chiSqRankingList(FF3& cipher, size_t SampSize, u8* x1, u8* x2);

int main()
{
    size_t input_size  = 1;
    size_t domain_size = 10;
    size_t nb_rounds  = 8;

    const double q0 = (nb_rounds / 2 - 1.5) * std::log2(domain_size);

    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distribution(0, domain_size - 1);
 
    // -4 0.56000 0.58520 0.02520
    // -2 0.44000 0.53720 0.09720
    //  0 0.27400 0.65270 0.37870
    //  2 0.04300 0.95580 0.91280
    //  4 0.00000 1.00000 1.00000
    std::vector<double> thresholds {0.56000, 0.44000, 0.27400, 0.04300, 0.00000};
    std::vector<int> data          {     -4,      -2,       0,       2,       8};
    std::vector<size_t> trials     {   1024,    1024,    1024,    1024,     128};

    std::cout << std::fixed << std::setprecision(5);
    for(size_t i = 4; i < data.size(); ++i) {
        size_t nb_success = 0;
        const size_t N = std::pow(2, data[i] + q0);
        std::cout << N << std::endl;
        const double t = thresholds[i];
        std::cout << "::: case " << std::setw(2) << i << " :::" << std::endl;
        std::cout << "Data:      " << std::setw(8) << data[i] << std::endl;
        std::cout << "Trials:    " << std::setw(8) << trials[i] << std::endl;
        std::cout << "Threshold: " << std::setw(8) << t << std::endl;
        std::cout << "..." << std::endl;

        std::uniform_int_distribution<> distribution(0, domain_size - 1);
        #pragma omp parallel for reduction(+:nb_success)
        for(size_t k = 0; k < trials[i]; ++k) {
            std::mt19937 gen(rd());

            u8 key[16];
            fillRandom(key, 16, gen);
            FF3 ctx(nb_rounds, input_size, domain_size, key, gen);
            
            // Known message
            std::vector<u8> x1(2 * input_size);
            u64_to_bytes(distribution(gen), input_size, x1.data());
            const u64 right_input = distribution(gen);
            u64_to_bytes(right_input, input_size, x1.data() + input_size);
            // Secret message
            std::vector<u8> x2(2 * input_size);
            const u64 target = distribution(gen);
            u64_to_bytes(target, input_size, x2.data());
            u64_to_bytes(right_input, input_size, x2.data() + input_size);

            std::vector<size_t> x = FF3_chiSqRankingList(ctx, N, x1.data(), x2.data());
            const auto end = x.begin() + t * x.size() + 1;
            if(std::find(x.begin(), end, target) != end)
                ++nb_success;
            std::cout << "#Success:  " << std::setw(3) << nb_success
                      << " ["    << std::setw(3) << k + 1
                      << " of " << std::setw(3) << trials[i] << "]" << std::endl;
        }
        std::cout << "#Success:  " << std::setw(3) << nb_success << std::endl;
    }
}

std::vector<size_t> FF3_chiSqRankingList(FF3& cipher, size_t SampSize, u8* x1, u8* x2)
{
    u8 tweak[8] ={ 0 };
    fillRandom_fillZero(tweak + 4, 4, cipher.gen); // T_L is fixed
    
    std::vector<double> PrD1 = FF3_fixedInputPrDistribution(cipher, tweak, SampSize, x1);
    std::vector<double> PrD2 = FF3_fixedInputPrDistribution(cipher, tweak, SampSize, x2);
    
    std::vector<double> distance(cipher.domain_size, 0);
    
    // Compute Euclidean distances
    for (u64 i = 0; i < cipher.domain_size; ++i) {
        const int64_t delta = i - bytes_to_uint<u64>(x1, cipher.input_size);
        for (u64 j = 0; j < cipher.domain_size; ++j) {
            u64 k = (j - delta + cipher.domain_size) % cipher.domain_size;
            distance[i] += std::pow((PrD1[k] - PrD2[j]) / SampSize, 2);
        }
    }
    std::vector<size_t> indices(cipher.domain_size);
    std::iota(indices.begin(), indices.end(), 0); //Initializing
    std::sort(indices.begin(), indices.end(), [&distance] (size_t i, size_t j) {
        return distance[i] < distance[j];
    });

    return indices;
}
