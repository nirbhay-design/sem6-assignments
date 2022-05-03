load("common.sage")

def compoundSample(domain_size, Y, q):
    Z = np.zeros(Y.shape[0])
    for i in range(Y.shape[0]):
        X = np.random.multinomial(q, Y[i, :])
        Z[i] = np.sum((X - q / domain_size) ** 2) / (q / domain_size)
    Z.sort()
    return Z

def avgAdvantage(domain_size, falsePositiveRate, sample):
    t = chi2.ppf(1 - falsePositiveRate, domain_size - 1)
    p = 1 - np.searchsorted(sample, t) / len(sample)
    return p - falsePositiveRate


def maxAdvantage(domain_size, sample):
    return find_local_maximum(lambda x : avgAdvantage(domain_size, x, sample), 0, 1)

nb_rounds = 12
domain_size = 16

#X = makeSample(domain_size, nb_rounds // 2 - 1, 1600000, Cipher.FEA1)
X = makeSample(domain_size, nb_rounds // 2 - 1, 160000, Cipher.FEA1)

#for log_q in np.linspace(13, 30, 75):
log_q0 = (nb_rounds / 2 - 1.5) * log(domain_size, 2)
for offset in [-2, 0, 2, 4, 6]:
    log_q = log_q0 + offset
    sample = compoundSample(domain_size, X, 2^log_q)
    (a, p) = maxAdvantage(domain_size, sample)
    t = chi2.ppf(1 - p, domain_size - 1)

    print("({:02.5}, {:02.5}, {:02.4}, {:01.4}, {:01.4}),".format(t, p, float(log_q), a + p, a))
