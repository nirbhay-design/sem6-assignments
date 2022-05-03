load("common.sage")

def makeCompoundSample(domain_size, nb_rounds, q, sample, cipher):
    
    result = np.zeros(sample.shape[0])
    for i in range(sample.shape[0]):
        X1 = np.random.multinomial(q, sample[i, :]) / q
        X2 = np.random.multinomial(q, sample[i, :]) / q

        reference = np.sum(np.square(np.abs(X1 - X2))) / domain_size
        # Random function mapping right half to first round output
        random_function = np.random.randint(domain_size, size = domain_size)
        for delta in range(1, domain_size):
            # Different right hand side, resample
            if random_function[delta]:
                probabilities = makeSample(domain_size, nb_rounds // 2 - 1, 1, cipher)[0, :]
            else:
                probabilities = sample[i, :]
            X2 = np.random.multinomial(q, probabilities) / q

            diff = np.sum(np.square(np.abs(X1 - X2))) / domain_size
            if diff < reference:
                result[i] += 1
        result[i] /= domain_size

    return result

def averageAdvantage(domain_size, sorted_sample, falsePositiveRate):
    i = np.searchsorted(sorted_sample, falsePositiveRate, "right")
    return float(i) / len(sorted_sample) - falsePositiveRate

def maxAdvantage(domain_size, nb_rounds, q, sample, cipher):
    sorted_sample = makeCompoundSample(domain_size, nb_rounds, q, sample, cipher)
    sorted_sample = np.sort(sorted_sample)

    return find_local_maximum(
        lambda x : averageAdvantage(domain_size, sorted_sample, x), 0, 1
    )

#nb_rounds = 12
#domain_size = 256
#cipher = Cipher.FEA1
nb_rounds = 8
domain_size = 1000
cipher = Cipher.FF3

log_q0 = (nb_rounds // 2 - 2 + .5) * np.log2(domain_size)

sample = makeSample(domain_size, nb_rounds // 2 - 1, 2000, cipher)

#for offset in np.linspace(-6, 12, 75):
for offset in [-4, -2, 0, 2, 4]:
    log_q = log_q0 + offset
    q = int(2 ** log_q)
    (a, p) = maxAdvantage(domain_size, nb_rounds, q, sample, cipher)

    print("{:.5f} {:.5f} {:.5f} {:.5f} {:.5f}".format(offset, log_q, p, a + p, a))
    #print("{:.5f} {:.5f}".format(offset, a))


