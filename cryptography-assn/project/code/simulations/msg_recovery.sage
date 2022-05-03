load("common.sage")

def parity(x):
    return np.binary_repr(x).count('1') % 2

def makeCompoundSample(domain_size, nb_rounds, q, sample, cipher):
    
    result = np.zeros(sample.shape[0])
    for i in range(sample.shape[0]):
        X1 = np.random.multinomial(q, sample[i, :]) / q
        X2 = np.random.multinomial(q, sample[i, :]) / q

        X1 = fourierTransform(X1, cipher)[1:]
        X2 = fourierTransform(X2, cipher)[1:]

        reference = np.sum(np.square(np.abs(X1 - X2)))
        if cipher == Cipher.FF3:
            ks = complex(0, 2*pi) * np.array(range(1, domain_size)) / domain_size
        else:
            ks = np.array(range(1, domain_size), dtype="int64")
        for delta in range(1, domain_size):
            if cipher == Cipher.FF3:
                t = X1 - np.exp(delta * ks) * X2
            elif cipher == Cipher.FEA1:
                t = X1 - np.array([(-1) ** parity(np.int64(delta) & k) for k in ks]) * X2
            diff = np.real(np.inner(np.conjugate(t), t))
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
#domain_size = 16
#cipher = Cipher.FEA1
nb_rounds = 8
domain_size = 1000
cipher = Cipher.FF3

log_q0 = (nb_rounds // 2 - 2 + .5) * np.log2(domain_size)

#sample = makeSample(domain_size, nb_rounds // 2 - 1, 1000000, cipher)
sample = makeSample(domain_size, nb_rounds // 2 - 1, 1000, cipher)

offsets = [-4, -2, 0, 2, 4]

for offset in np.linspace(-6, 12, 75):
    log_q = log_q0 + offset
    q = int(2 ** log_q)
    (a, p) = maxAdvantage(domain_size, nb_rounds, q, sample, cipher)

    #print("{:.5f} {:.5f} {:.5f} {:.5f} {:.5f}".format(offset, log_q, p, a + p, a))
    print("{:.5f} {:.5f}".format(offset, a))
