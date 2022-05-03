import itertools
load("common.sage")

def avgAdvantage(falsePositiveRate, q, sample):
    result = 0

    s = float(sqrt(q))
    t = norm.ppf(1 - falsePositiveRate / 2)
    for x in sample:
        result += norm.cdf(s * x - t) - norm.cdf(s * x + t)
    result = 1 + result / len(sample)
    return result - falsePositiveRate

def maxAdvantage(q, sample):
    return find_local_maximum(lambda x : avgAdvantage(x, q, sample), 0, 1, tol = 1e-3)

def makeSampleFEA2(domain_size, r, sample_size):
    sample = np.zeros(sample_size)
    for i in range(sample_size):
        t = np.ones(domain_size - 1)
        for _ in range(r // 2):
            C1 = np.random.binomial(domain_size, 1/2, size = (domain_size - 1, domain_size - 1))
            C1 = (2. / domain_size) * C1 - 1
            C2 = np.random.binomial(domain_size, 1/2, size = (domain_size - 1, domain_size - 1))
            C2 = (2. / domain_size) * C2 - 1
            C = np.multiply(C1, C2)
            t = np.dot(C, t)

        sample[i] = t[0]

    return sample

nb_rounds = 18
domain_size = 16

# FEA-2
nb_rounds_effective = 2 * nb_rounds / 3 - 2

sample = makeSampleFEA2(domain_size, nb_rounds_effective, 50000)

log_q0 = (nb_rounds_effective / 2) * log(domain_size, 2)

#for log_q in np.linspace(log_q0 - 6, log_q0 + 13, 75):
for d in [-2, 0, 2, 4, 6]:
    log_q = log_q0 + d
    (a, p) = maxAdvantage(2 ** log_q, sample)

    t = chi.ppf(1 - p, df = 1)
    print("({:02.5}, {:02.4}, {:02.4}, {:01.4}, {:01.4}),".format(t, float(log_q), p, a + p, a))
    #print("{:02.4} {:01.4}".format(float(log_q - log_q0), a))
