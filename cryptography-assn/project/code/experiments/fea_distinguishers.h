#ifndef FEA_DISTINGUISHERS_H_INCLUDE_GUARD
#define FEA_DISTINGUISHERS_H_INCLUDE_GUARD

#include "common/fea.h"
#include <cstring>

double FEA1_fixedInputLinearDistinguisher(FEAContext& ctx, u64 mask, size_t SampSize)
{
    ctx.tweak->tweak[0] = randomU64(ctx.gen); //this tweak is fixed
    
    fillRandom(ctx.data[0].value, 16, ctx.gen);
    double c = 0;
    for (size_t j = 0; j < SampSize; ++j) {
        ctx.tweak->tweak[1] = randomU64(ctx.gen); //random tweak
        FEA_Encrypt(ctx.data + 1, ctx.data, ctx.tweak, ctx.encrypt_ctx);
        
        BytesToU64LR(ctx.data[1].value, ctx.output, ctx.block_size, !ctx.odd_nb_rounds);
        c += 1 - 2 * parity(mask & ctx.output[ctx.odd_nb_rounds]);
    }

    return c / SampSize;
}

std::vector<double> FEA1_PrDistribution(FEAContext& ctx, u64 SampSize, u8* x1)
{
    const size_t lenLeft = std::ceil(ctx.block_size / 2.);
    const size_t lenRight = ctx.block_size / 2;

    const size_t lenHistogram = ctx.odd_nb_rounds ? lenRight : lenLeft;
    std::vector<double> PrD(std::pow(2, lenHistogram), 0);
    
    std::memcpy(ctx.data[0].value, x1, 16);
    for (size_t i = 0; i < SampSize; ++i) {
        ctx.tweak->tweak[1] = randomU64(ctx.gen);
        FEA_Encrypt(ctx.data + 1, ctx.data, ctx.tweak, ctx.encrypt_ctx);
        BytesToU64LR(ctx.data[1].value, ctx.output, ctx.block_size, !ctx.odd_nb_rounds);
        PrD[ctx.output[ctx.odd_nb_rounds] >> (64 - lenHistogram)] += 1;
    }
    return PrD;
}

double FEA1_chiSqDistinguisher(FEAContext& ctx, u64 mask, size_t SampSize)
{
    ctx.tweak->tweak[0] = randomU64(ctx.gen); //this tweak is fixed

    int lenRight = floor(ctx.block_size / 2);
    fillRandom(ctx.data[0].value, 16, ctx.gen);
    // Note: here all of the input is kept fixed, but actually the left side can be variable
    std::vector<double> histogram = FEA1_PrDistribution(ctx, SampSize, ctx.data[0].value);

    const double expected_count = SampSize / std::pow(2, lenRight);
    double sum = 0;
    for(double x : histogram)
        sum += std::pow(x - expected_count, 2) / expected_count;
    return sum;
}

double FEA2_fixedInputLinearDistinguisher(FEAContext& ctx, u64 mask, size_t SampSize)
{
    const int lenLeft = std::ceil(ctx.block_size / 2.);
    ctx.tweak->tweak[0] = randomU64(ctx.gen);
    ctx.tweak->tweak[1] = randomU64(ctx.gen);
    
    fillRandom(ctx.data[0].value, 16, ctx.gen);
    
    double c = 0;
    for (size_t i = 0; i < SampSize; ++i) {
        ctx.tweak->tweak[1] ^= randomU64(ctx.gen) >> lenLeft;
        
        FEA_Encrypt(ctx.data + 1, ctx.data, ctx.tweak, ctx.encrypt_ctx);
        
        BytesToU64LR(ctx.data[1].value, ctx.output, ctx.block_size, !ctx.odd_nb_rounds);
        c += 1 - 2 * parity(mask & ctx.output[ctx.odd_nb_rounds]);
    }
    return c / SampSize;
}

double FEA2_chiSqDistinguisher(FEAContext& ctx, u64, size_t SampSize)
{
    const size_t lenLeft = std::ceil(ctx.block_size / 2.);
    const size_t lenRight = ctx.block_size / 2;

    ctx.tweak->tweak[0] = randomU64(ctx.gen);
    ctx.tweak->tweak[1] = randomU64(ctx.gen);
    fillRandom(ctx.data[0].value, 16, ctx.gen);
    
    const size_t lenHistogram = ctx.odd_nb_rounds ? lenRight : lenLeft;
    std::vector<size_t> histogram(std::pow(2, lenHistogram), 0);
    
    for (size_t i = 0; i < SampSize; ++i) {
        ctx.tweak->tweak[1] ^= randomU64(ctx.gen) >> lenLeft;
    
        FEA_Encrypt(ctx.data + 1, ctx.data, ctx.tweak, ctx.encrypt_ctx);
        
        BytesToU64LR(ctx.data[1].value, ctx.output, ctx.block_size, !ctx.odd_nb_rounds);
        histogram[ctx.output[ctx.odd_nb_rounds] >> (64 - lenHistogram)] += 1;
    }
    const double expected_count = SampSize / std::pow(2, lenHistogram);
    double sum = 0;
    for(double x : histogram)
        sum += std::pow(x - expected_count, 2) / expected_count;
    return sum;
}

#endif
