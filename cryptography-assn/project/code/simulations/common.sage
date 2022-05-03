from enum import Enum
import numpy as np
from scipy.stats import norm
from scipy.stats import chi
from scipy.stats import chi2

class Cipher(Enum):
    FEA1 = 0
    FEA2 = 1
    FF3  = 2

FT = np.array([[1, 1], [1, -1]])

def fourierTransform_F2(X):
    if X.shape[0] == 2:
        return np.matmul(FT, X)

    l = X.shape[0] / 2
    A = fourierTransform_F2(X[:l])
    B = fourierTransform_F2(X[l:])
    return np.concatenate((A + B, A - B))

def fourierTransform(X, cipher):
    if cipher == Cipher.FEA1 or cipher == Cipher.FEA2:
        Y = np.swapaxes(X, -1, 0)
        Y = fourierTransform_F2(Y)
        return np.swapaxes(Y, -1, 0)
    elif cipher == Cipher.FF3:
        return np.fft.fft(X)

def inverseFourierTransform(X, cipher):
    if cipher == Cipher.FEA1 or cipher == Cipher.FEA2:
        Y = np.swapaxes(X, -1, 0)
        Y = fourierTransform_F2(Y) / Y.shape[0]
        return np.swapaxes(Y, -1, 0)
    elif cipher == Cipher.FF3:
        return np.fft.ifft(X)

def makeSample_FEA2(domain_size, nb_rounds_effective, sample_size):
    sample = np.zeros([sample_size, domain_size])
    for i in range(sample_size):
        t = np.ones(domain_size - 1)
        for _ in range(nb_rounds_effective):
            # Approximation: independent correlations for random function
            C1 = np.random.binomial(domain_size, 1/2, size = (domain_size - 1, domain_size - 1))
            C1 = (2. / domain_size) * C1 - 1
            C2 = np.random.binomial(domain_size, 1/2, size = (domain_size - 1, domain_size - 1))
            C2 = (2. / domain_size) * C2 - 1
            C = np.multiply(C1, C2)
            t = np.dot(C, t)

        sample[i, :] = np.concatenate([[1], t])

    return inverseFourierTransform(sample, Cipher.FEA2)


def makeSample(domain_size, nb_rounds_effective, sample_size, cipher):
    # Each row of c contains a sample of domain_size correlations
    if cipher == Cipher.FEA1:
        c = np.ones((sample_size, domain_size))
    elif cipher == Cipher.FEA2:
        return makeSample_FEA2(domain_size, nb_rounds_effective, sample_size)
    elif cipher == Cipher.FF3:
        c = np.ones((sample_size, domain_size), dtype = "complex128")
    for _ in range(nb_rounds_effective):
        X = np.random.multinomial(
            domain_size, [1/domain_size] * domain_size,
            size = sample_size
        )
        X = fourierTransform(X, cipher) / domain_size
        c *= X
    p_real = np.real(inverseFourierTransform(c, cipher))
    return p_real
