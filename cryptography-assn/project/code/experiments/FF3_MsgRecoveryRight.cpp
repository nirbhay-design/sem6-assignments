#include <iostream>
#include <iomanip>

#include "ff3_distinguishers.h"

std::vector<size_t> FF3_chiSqRankingList(FF3& cipher, size_t SampSize, u8* x);

int main()
{
    size_t input_size  = 1;
    size_t domain_size = 10;
    size_t nb_rounds  = 8;

    const double q0 = (nb_rounds / 2 - 1.5) * std::log2(domain_size);

    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distribution(0, domain_size - 1);
 
    // -4.00000 0.11900 0.14900 0.03000
    // -2.00000 0.36700 0.42600 0.05900
    //  0.00000 0.39800 0.71700 0.31900
    //  2.00000 0.07700 0.93700 0.86000
    //  4.00000 0.00000 1.00000 1.00000
    std::vector<double> thresholds {0.11900, 0.36700, 0.39800, 0.07700, 0.00000};
    std::vector<int> data          {     -4,      -2,       0,       2,       8};
    std::vector<size_t> trials     {   1024,    1024,    1024,    1024,     128};

    std::cout << std::fixed << std::setprecision(5);
    for(size_t i = 4; i < data.size(); ++i) {
        size_t nb_success = 0;
        const size_t N = std::pow(2, data[i] + q0);
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
            
            // Secret right half message
            std::vector<u8> x_right(input_size, 0);
            const u64 target = distribution(gen);
            u64_to_bytes(target, input_size, x_right.data());

            std::vector<size_t> x = FF3_chiSqRankingList(ctx, N, x_right.data());
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

std::vector<size_t> FF3_chiSqRankingList(FF3& cipher, size_t SampSize, u8* x_right)
{
    u8 tweak[8] ={ 0 };
    fillRandom_fillZero(tweak + 4, 4, cipher.gen); // T_L is fixed
    
    std::vector<double> PrD1 = FF3_PrDistribution(cipher, tweak, SampSize, x_right);
    
    std::vector<double> distance(cipher.domain_size, 0);
    
    // Compute Euclidean distances
    for (u64 i = 0; i < cipher.domain_size; ++i) {
        std::vector<u8> guess(cipher.input_size, 0);
        u64_to_bytes(i, cipher.input_size, guess.data());

        std::vector<double> PrD2 = FF3_PrDistribution(cipher, tweak, SampSize, guess.data());
        for (u64 j = 0; j < cipher.domain_size; ++j)
            distance[i] += std::pow((PrD1[j] - PrD2[j]) / SampSize, 2);
    }
    std::vector<size_t> indices(cipher.domain_size);
    std::iota(indices.begin(), indices.end(), 0); //Initializing
    std::sort(indices.begin(), indices.end(), [&distance] (size_t i, size_t j) {
        return distance[i] < distance[j];
    });

    return indices;
}
