#include <iostream>
#include <iomanip>

#include "ff3_distinguishers.h"

int main(int argc, char** argv) {
    size_t input_size  = 1;
    size_t domain_size = 100;
    size_t nb_rounds  = 8;

    const double q0 = (nb_rounds / 2 - 1) * std::log2(domain_size);

    std::vector<double> thresholds { 1.0981, 1.2223, 1.3757, 1.5552, 1.7503 };
    std::vector<int> data          {     -2,      0,      2,      4,     6  };
    std::vector<size_t> trials     {   1024,   1024,   1024,   1024,   1024 };

    std::cout << std::fixed << std::setprecision(5);
    for(size_t i = 0; i < data.size(); ++i) {
        size_t nb_success = 0;
        const size_t N = std::pow(2, data[i] + q0);
        const double t = thresholds[i] / std::sqrt(N);
        std::cout << "::: case " << std::setw(2) << i << " :::" << std::endl;
        std::cout << "Data:      " << std::setw(8) << data[i] << std::endl;
        std::cout << "Trials:    " << std::setw(8) << trials[i] << std::endl;
        std::cout << "Threshold: " << std::setw(8) << t << std::endl;
        std::cout << "..." << std::endl;

        std::uniform_int_distribution<> distribution(1, domain_size - 1);
        #pragma omp parallel for reduction(+:nb_success)
        for(size_t k = 0; k < trials[i]; ++k) {
            std::mt19937 gen(rd());

            u8 key[16];
            fillRandom(key, 16, gen);
            FF3 ctx(nb_rounds, input_size, domain_size, key, gen);
            const u64 mask = distribution(gen);
            
            const double c = std::abs(FF3_fixedInputLinearDistinguisher(ctx, mask, N));
            if(c > t)
                ++nb_success;
            std::cout << "#Success:  " << std::setw(3) << nb_success
                      << " ["    << std::setw(3) << k + 1
                      << " of " << std::setw(3) << trials[i] << "]" << std::endl;
        }
        std::cout << "#Success:  " << std::setw(3) << nb_success << std::endl;
    }

}
