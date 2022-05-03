import itertools
import numpy as np
from scipy.stats import norm
from scipy.stats import chi

def successRateLinear(c, falsePositiveRate, N):
    #c = abs(c)
    s = float(sqrt(N))
    t = norm.ppf(1 - falsePositiveRate / 2)
    return norm.cdf(s * c - t) - norm.cdf(s * c + t) + 1

def productDistribution(dist_1, dist_2):
    dist = dict()
    for (x, p) in dist_1.items():
        for (y, q) in dist_2.items():
            dist[x * y] = dist.get(x * y, 0) + p * q
    return dist

def correlationDistribution(r, n):
    distribution = dict()
    m = n // 2
    dist_ideal = {
        k / 2^(m-1) : binomial(2^m, 2^(m - 1) + k) / 2^(2^m)\
        for k in range(-2^(m - 1), 2^(m - 1) + 1)
    }

    distribution = copy(dist_ideal)
    for _ in range(r // 2 - 1):
        distribution = productDistribution(distribution, dist_ideal)
    return distribution

def avgSuccessRateLinear(falsePositiveRate, q, dist):
    success_rate = 0
    for c, p in dist.items():
        success_rate += successRateLinear(c, falsePositiveRate, q) * p
    return success_rate

def avgAdvantage(falsePositiveRate, q, dist = None):
    return avgSuccessRateLinear(falsePositiveRate, q, dist)\
            - falsePositiveRate

def avgAdvantageMC(falsePositiveRate, q, sample):
    result = 0

    s = float(sqrt(q))
    t = norm.ppf(1 - falsePositiveRate / 2)
    for x in sample:
        result += norm.cdf(s * x - t) - norm.cdf(s * x + t)
    result = 1 + result / len(sample)
    return result - falsePositiveRate

def maxAdvantage(q, dist):
    return find_local_maximum(lambda x : avgAdvantage(x, q, dist), 0, 1)

def maxAdvantageMC(q, sample):
    return find_local_maximum(lambda x : avgAdvantageMC(x, q, sample), 0, 1, tol = 1e-3)

def makeSampleFEA1(r, n):
    m = n // 2
    std = 2^(-m)
    X = np.random.multivariate_normal(
        np.zeros(r // 2), cov = std * np.identity(r // 2), size = (10000, )
    )
    #X = 2^(1 - m) * np.random.binomial(2^m, 1/2, size = (10000, r // 2)) - 1 
    return np.prod(X, 1)

nb_rounds = 12
block_size = 8

dist = correlationDistribution(nb_rounds - 2, block_size) # Exact (small block_size only)
#sample = makeSampleFEA1(nb_rounds - 2, block_size) # Monte-Carlo

log_q0 = (nb_rounds // 2 - 1) * block_size // 2
#for log_q in np.linspace(log_q0 - 6, log_q0 + 12, 50):
for log_q in [log_q0 - 2, log_q0, log_q0 + 2, log_q0 + 4, log_q0 + 6]:
    (a, p) = maxAdvantage(2 ^ log_q, dist)
    #(a, p) = maxAdvantageMC(2 ^ log_q, sample)
    print("({:02.5}, {:02.4}, {:01.4}, {:01.4}),".format(p, float(log_q), a + p, a))
    #print("{:02.5} {:02.4}".format(float(log_q - log_q0 + 20), a))
