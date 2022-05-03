#include <iostream>
#include <iomanip>
#include "fea_distinguishers.h"

int main(int argc, char** argv) {
    size_t block_size = 8;
    size_t nb_rounds  = 18;

    std::vector<double> thresholds { 1.073, 1.170, 1.333, 1.562, 1.838 };
    std::vector<size_t> data       {    18,    20,    22,    24,    26 };
    std::vector<size_t> trials     {   512,   512,   512,   512,   512 };

    std::uniform_int_distribution<> distribution(1, 15);
    std::cout << std::fixed << std::setprecision(5);
    for(size_t i = 0; i < data.size(); ++i) {
        size_t nb_success = 0;
        const size_t N = std::pow(2, data[i]);
        const double t = thresholds[i] / std::sqrt(N);
        std::cout << "::: case " << std::setw(2) << i << " :::" << std::endl;
        std::cout << "Data:      " << std::setw(8) << data[i] << std::endl;
        std::cout << "Trials:    " << std::setw(8) << trials[i] << std::endl;
        std::cout << "Threshold: " << std::setw(8) << t << std::endl;
        std::cout << "..." << std::endl;

        #pragma omp parallel for reduction(+:nb_success)
        for(size_t k = 0; k < trials[i]; ++k) {
            std::mt19937 gen(rd());
            FEAContext ctx(FEA_ALG_ID_FEA_B, 128, block_size, nb_rounds, gen);
            const u64 mask = u64(distribution(ctx.gen)) << (64 - block_size / 2);
            
            const double c = std::abs(FEA2_fixedInputLinearDistinguisher(ctx, mask, N));
            if(c > t)
                ++nb_success;
            std::cout << "#Success:  " << std::setw(3) << nb_success
                      << " ["    << std::setw(3) << k + 1
                      << " of " << std::setw(3) << trials[i] << "]" << std::endl;
        }
        std::cout << "#Success:  " << std::setw(3) << nb_success << std::endl;
    }

}
