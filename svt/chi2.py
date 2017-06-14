from collections import Counter as Freq
from scipy.stats import chi2
from random import random


def is_rejected(pvalue, alpha):
    """Is the hypothesis rejected given alpha and pvalue?"""
    return pvalue <= alpha


def chi2_t(sample, p):
    a, b = min(p), max(p)
    freqs = Freq(sample)

    n = sum(freqs.values())
    t = sum([(freqs[i] - n * p[i]) ** 2 / (n * p[i]) for i in range(a, b + 1)])
    return t


def chi2_test(sample, p, m=0):
    """Return the chi squared statistic and its pvalue.

    :param sample: sample
    :param p: hypothesized probability distribution
    :param m: number of unknown parameters

    :type p: dict(number, float)
    :type sample: list(number) or dictionary of frequencies
    :return: t, pvalue

    Examples:
    >>> p = {0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4}
    >>> sample = [0, 1, 1, 2, 2, 2, 3, 3, 3, 3]
    >>> t, pvalue = chi2_test(p, sample)

    >>> def estimate(sample):
    >>>    lam = 2.9
    >>>    n = len(sample)
    >>>    p = {i: exp(-lam) * lam ** i / factorial(i) for i in range(n - 1)}
    >>>    p[n - 1] = 1 - sum(p.values())
    >>>    return p
    >>> sample = {0: 6, 1: 2, 2: 1, 3: 9, 4: 7, 5: 5}
    >>> t, pvalue = chi2_test(sample, estimate(sample), 1)
    """
    k = max(p) - min(p) + 1
    t = chi2_t(sample, p)
    pvalue = 1 - chi2.cdf(t, k - 1 - m)
    return t, pvalue


def inverse_transform(p):
    """Get a random value given a discrete distribution.

    :param p: probability distribution
    :type p: dict(number, float)
    """
    ps = list(p.values())
    xs = list(p.keys())
    U = random()
    i = 0
    F = ps[0]
    while U >= F:
        i += 1
        F += ps[i]
    return xs[i]


def chi2_test_unk_params(n, p, t, estimate_p, niter):
    """
    >>> def estimate(sample, lam=None):
    >>>     from math import exp, factorial
    >>>     n = len(Freq(sample))
    >>>     if lam is None:
    >>>         lam = sum(sample) / n
    >>>     p = {i: exp(-lam) * lam ** i / factorial(i) for i in range(n - 1)}
    >>>     p[n - 1] = 1 - sum(p.values())
    >>>     return p

    >>> sample = list(Freq({0: 6, 1: 2, 2: 1, 3: 9, 4: 7, 5: 5}).elements())
    >>> n = len(sample)
    >>> p = estimate(sample, 2.9)
    >>> t = chi2_t(sample, p)

    >>> t, pvalue = chi2_test_unk_params(n, p, t, estimate, 100000)
    """
    pvalue = 0
    for i in range(niter):
        generated_sample = [inverse_transform(p) for _ in range(n)]
        p = estimate_p(generated_sample)
        ti = chi2_t(generated_sample, p)
        if ti >= t:
            pvalue += 1
    return t, pvalue / niter
