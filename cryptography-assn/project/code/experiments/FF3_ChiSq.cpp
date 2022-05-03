#include <iostream>
#include <iomanip>

#include "ff3_distinguishers.h"

int main(int argc, char** argv) {
    size_t input_size  = 2;
    size_t domain_size = 1000;
    size_t nb_rounds  = 8;

    const double q0 = (nb_rounds / 2 - 2 + .5) * std::log2(domain_size);


    // -4 998.49351  0.51633 0.01776,
    // -2 1001.41268 0.54347 0.07091,
    //  0 1013.11900 0.64330 0.27233,
    //  2 1058.76162 0.90105 0.80864,
    //  4 1191.14173 0.99999 0.99996,
    std::vector<double> thresholds {998.49351, 1001.41268, 1013.11900, 1058.76162, 1191.14173};

    std::vector<int> data          {       -4,         -2,          0,          2,          4};
    std::vector<size_t> trials     {     1024,       1024,       1024,       1024,       1024};

    std::cout << std::fixed << std::setprecision(5);
    for(size_t i = 0; i < data.size(); ++i) {
        size_t nb_success = 0;
        const size_t N = std::pow(2, data[i] + q0);
        std::cout << N << std::endl;
        const double t = thresholds[i];
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
            
            const double x = FF3_chiSqDistinguisher(ctx, 0, N);
            if(x > t)
                ++nb_success;
            std::cout << "#Success:  " << std::setw(3) << nb_success
                      << " ["    << std::setw(3) << k + 1
                      << " of " << std::setw(3) << trials[i] << "]" << std::endl;
        }
        std::cout << "#Success:  " << std::setw(3) << nb_success << std::endl;
    }

}
