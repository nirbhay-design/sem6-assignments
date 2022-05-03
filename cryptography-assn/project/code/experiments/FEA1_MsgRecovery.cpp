#include <iostream>
#include <iomanip>

#include "fea_distinguishers.h"

std::vector<size_t> FEA1_chiSqRankingList(FEAContext& ctx, size_t SampSize, u8* x1, u8* x2);

int main()
{
    size_t block_size = 8;
    size_t nb_rounds  = 12;

    std::mt19937 gen(rd());
 
    //  -4 14.00000 0.37500 0.45823 0.08323
    //  -2 16.00000 0.37500 0.49722 0.12222
    //   0 18.00000 0.37500 0.59305 0.21805
    //   2 20.00000 0.37500 0.74152 0.36652
    //   4 22.00000 0.31250 0.83951 0.52701
    std::vector<double> thresholds {0.37500, 0.37500, 0.37500, 0.37500, 0.31250};
    std::vector<int> data          {  14,  16,  18,  20,  22 };
    std::vector<size_t> trials     { 512, 512, 512, 512, 512 };

    std::cout << std::fixed << std::setprecision(5);
    for(size_t i = 0; i < data.size(); ++i) {
        size_t nb_success = 0;
        const size_t N = std::pow(2, data[i]);
        std::cout << N << std::endl;
        const double t = thresholds[i];
        std::cout << "::: case " << std::setw(2) << i << " :::" << std::endl;
        std::cout << "Data:      " << std::setw(8) << data[i] << std::endl;
        std::cout << "Trials:    " << std::setw(8) << trials[i] << std::endl;
        std::cout << "Threshold: " << std::setw(8) << t << std::endl;
        std::cout << "..." << std::endl;

        std::uniform_int_distribution<> distribution(0, std::pow(2, block_size / 2) - 1);
        #pragma omp parallel for reduction(+:nb_success)
        for(size_t k = 0; k < trials[i]; ++k) {
            std::mt19937 gen(rd());

            u8 key[16];
            fillRandom(key, 16, gen);
            FEAContext ctx(FEA_ALG_ID_FEA_A, 128, block_size, nb_rounds, gen);
            
            // Known message
            std::vector<u8> x1(16, 0);
            fillRandom(x1.data(), x1.size(), gen); // Extra bytes will be ignored
            u64 x1_halves[2] {};
            BytesToU64LR(x1.data(), x1_halves, ctx.block_size, 0);
            // Secret message (same right hand side)
            u64 x2_halves[2] {};
            const u64 target = distribution(gen);
            x2_halves[0] = target << (64 - ctx.block_size / 2);
            x2_halves[1] = x1_halves[1];
            std::vector<u8> x2(16, 0);
            U64LRToBytes(x2_halves, x2.data(), ctx.block_size, 0);

            std::vector<size_t> x = FEA1_chiSqRankingList(ctx, N, x1.data(), x2.data());
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

std::vector<size_t> FEA1_chiSqRankingList(FEAContext& ctx, size_t SampSize, u8* x1, u8* x2)
{
    ctx.tweak->tweak[0] = randomU64(ctx.gen);
    ctx.tweak->tweak[1] = randomU64(ctx.gen);
    
    u64 x1_halves[2] {};
    BytesToU64LR(x1, x1_halves, ctx.block_size, 0);
        
    std::vector<double> PrD1 = FEA1_PrDistribution(ctx, SampSize, x1);
    std::vector<double> PrD2 = FEA1_PrDistribution(ctx, SampSize, x2);
    
    std::vector<double> distance(std::pow(2, ctx.block_size / 2), 0);
    
    // Compute Euclidean distances
    for (size_t i = 0; i < PrD1.size(); ++i) {
        const size_t delta = i ^ (x1_halves[0] >> (64 - ctx.block_size / 2));
        for (size_t j = 0; j < PrD2.size(); ++j) {
            distance[i] += std::pow((PrD1[j ^ delta] - PrD2[j]) / SampSize, 2);
        }
    }
    std::vector<size_t> indices(distance.size());
    std::iota(indices.begin(), indices.end(), 0); //Initializing
    std::sort(indices.begin(), indices.end(), [&distance] (size_t i, size_t j) {
        return distance[i] < distance[j];
    });

    return indices;
}
