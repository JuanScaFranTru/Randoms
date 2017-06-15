from random import random
from collections import Counter as Freq
from math import sqrt
from scipy.stats import norm


def discrete_uniform(a, b):
    return int(random() * (b - a + 1)) + a


def permutation(A):
    for i in range(len(A) - 1, 0, -1):
        index = discrete_uniform(0, i)
        A[i], A[index] = A[index], A[i]
    return A


def range_(sample1, sample2):
    sample = sorted(sample1 + sample2)
    sample1, sample2 = sorted([sample1, sample2])
    freqs = Freq(sample)

    R = 0
    repeated = []
    for x, count in freqs.items():
        if count > 1:
            repeated.append(x)
            i = sample.index(x)
            R += sum([j for j in range(i + 1, i + count + 1)]) / count

    R += sum([i + 1 for i, s in enumerate(sample)
              if s in sample1 and s not in repeated])

    return R


def ranges(n, m, r):
    if (n, m) == (1, 0):
        if r <= 0:
            return 0
        else:
            return 1
    if (n, m) == (0, 1):
        if r < 0:
            return 0
        else:
            return 1
    else:
        if n == 0:
            return ranges(0, m - 1, r)
        elif m == 0:
            return ranges(n - 1, 0, r - n)
        else:
            return n / (n + m) * ranges(n - 1, m, r - n - m) + \
                m / (n + m) * ranges(n, m - 1, r)


def two_samples_small(sample1, sample2):
    """Return the exact p-value of H0: the samples are equally distributed."""
    sample1, sample2 = sorted([sample1, sample2])
    n, m = len(sample1), len(sample2)
    R = range_(sample1, sample2)

    sr = ranges(n, m, R)
    return 2 * min(1 - sr, sr)


def two_samples_normal(sample1, sample2):
    """Approximate the p-value of H0: the samples are equally distributed."""
    sample1, sample2 = sorted([sample1, sample2])
    n, m = len(sample1), len(sample2)

    R = range_(sample1, sample2)
    mean = n * (n + m + 1) / 2
    std_dev = sqrt(n * m * (n + m + 1) / 12)

    r_star = (R - mean) / std_dev

    if R <= mean:
        return 2 * norm.cdf(r_star)
    return 2 * (1 - norm.cdf(r_star))


def two_samples_sim(sample1, sample2, niter):
    """Approximate the p-value of H0: the samples are equally distributed."""
    sample = sample1 + sample2
    r = range_(sample1, sample2)
    a, b = 0, 0
    nm = len(sample)

    for _ in range(niter):
        perm = permutation(sample)
        R = sum([i + 1 for i in range(nm) if perm[i] in sample1])
        b += R >= r
        a += R <= r

    return 2 * min(b / niter, a / niter)
