import itertools

load("common.sage")

#disk_samples = np.random.normal(0, sqrt(.5), 70000) + 1j * np.random.normal(0, sqrt(.5), 70000)
disk_samples = np.random.normal(0, sqrt(.5), 10000) + 1j * np.random.normal(0, sqrt(.5), 10000)

def successRateLinear(c, t, sqrt_q):
    z = np.abs(c * sqrt_q + disk_samples)
    return np.count_nonzero(z > t) / z.size

def avgAdvantage(falsePositiveRate, q, sample):
    result = 0

    sqrt_q = float(sqrt(q))
    t = chi.ppf(1 - falsePositiveRate, df = 2) / np.sqrt(2)
    for x in sample:
        result += successRateLinear(x, t, sqrt_q)
    result = result / len(sample)
    return result - falsePositiveRate

def maxAdvantage(q, sample):
    return find_local_maximum(lambda x : avgAdvantage(x, q, sample), 0, 1, tol = 1e-4)

def makeSample(r, domain_size):
    var = 1 / (2 * domain_size)
    X = np.random.multivariate_normal(
        np.zeros(r // 2), cov = var * np.identity(r // 2), size = (10000, )
    )
    Y = np.random.multivariate_normal(
        np.zeros(r // 2), cov = var * np.identity(r // 2), size = (10000, )
    )
    return np.prod(X + 1j*Y, 1)


nb_rounds = 8
domain_size = 100 # Size of one branch

sample = makeSample(nb_rounds - 2, domain_size)

log_q0 = float((nb_rounds // 2 - 1) * log(domain_size, 2))

for log_q in np.linspace(log_q0 - 6, log_q0 + 12, 70):
    (a, p) = maxAdvantage(2 ^ log_q, sample)
    #print("({:02.5}, {:02.4}, {:01.4}, {:01.4}),".format(chi.ppf(1 - p, df = 2) / np.sqrt(2), float(log_q - log_q0), a + p, a))
    print("{:02.5} {:02.4}".format(float(log_q - log_q0), a))
