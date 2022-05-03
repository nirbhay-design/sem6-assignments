load("common.sage")

def makeCompoundSample(domain_size, sample_size, q, sample):
    result = np.zeros(sample_size * sample.shape[0])
    for i in range(sample.shape[0]):
        temp = np.random.multinomial(q, sample[i, :], size = sample_size)
        result[sample_size*i:sample_size*i+sample_size] = np.sum(np.square(temp - q / domain_size), 1) / (q / domain_size)
    return result

def averageAdvantage(domain_size, sorted_sample, falsePositiveRate):
    t = chi2.ppf(1 - falsePositiveRate, df = domain_size - 1)

    i = np.searchsorted(sorted_sample, t)
    return 1 - float(i) / len(sorted_sample) - falsePositiveRate

def maxAdvantage(domain_size, q, sample):
    #sorted_sample = makeCompoundSample(domain_size, 100000, q, sample)
    sorted_sample = makeCompoundSample(domain_size, 500, q, sample)
    sorted_sample = np.sort(sorted_sample)

    return find_local_maximum(
        lambda x : averageAdvantage(domain_size, sorted_sample, x),
        0, 1
    )

nb_rounds = 8
domain_size = 1000

log_q0 = (nb_rounds // 2 - 1.5) * np.log2(domain_size)

sample = makeSample(domain_size, nb_rounds // 2 - 1, 1000, Cipher.FF3)

for offset in np.linspace(-6, 6, 75):
#for offset in [-4, -2, 0, 2, 4]:
    q = int(2 ** (log_q0 + offset))
    (a, p) = maxAdvantage(domain_size, q, sample)
    t = chi2.ppf(1 - p, df = domain_size - 1)

    #print("{:2} {:.5f} {:.5f} {:.5f}".format(offset, t, a + p, a))
    print("{:.5f} {:.5f}".format(offset, a))
