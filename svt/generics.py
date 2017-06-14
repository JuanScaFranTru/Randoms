from collections import Counter as Freq
from collections import defaultdict
from scipy.stats import chi2
from random import random


def is_rejected(pvalue, alpha):
    """Is the hypothesis rejected given alpha and pvalue?"""
    return pvalue <= alpha


def chi2_test(sample, p):
    """Return the chi squared statistic and its pvalue.

    :param sample: sample
    :param p: hypothesized probability distribution

    :type p: dict(number, float)
    :type sample: list(number)
    :return: t, pvalue

    Example:
    >>> p = {0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4}
    >>> sample = [0, 1, 1, 2, 2, 2, 3, 3, 3, 3]
    >>> t, pvalue = chi2_test(p, sample)

    """
    a, b = min(p), max(p)
    k = b - a + 1
    n = len(sample)

    p = defaultdict(float, p)
    freqs = Freq(sample)

    t = sum([(freqs[i] - n * p[i]) ** 2 / (n * p[i]) for i in range(a, b + 1)])
    pvalue = 1 - chi2.cdf(t, k)

    return t, pvalue


def kolmogorov_test(sample, F, niter):
    """Return the kolmogorov-Smirnov statistic, its pvalue and its dis.

    Example:
    >>> def F(x): return 1 - exp(- x / 100)
    >>> sample = [66, 72, 81, 94, 112, 116, 124, 140, 145, 155]
    >>> d, pvalue, dis = kolmorogorov_test(sample, F, 500)

    """
    sample.sort()
    n = len(sample)
    accum = [F(s) for s in sample]
    diff1 = [(j + 1) / n - a for j, a in enumerate(accum)]
    diff2 = [a - j / n for j, a in enumerate(accum)]
    d = max(diff1 + diff2)

    pvalue = 0
    dis = [None] * niter
    for i in range(niter):
        uniforms = sorted([random() for _ in range(n)])
        uni_diff1 = [(j + 1) / n - u for j, u in enumerate(uniforms)]
        uni_diff2 = [u - j / n for j, u in enumerate(uniforms)]
        dis[i] = max(uni_diff1 + uni_diff2)
        if dis[i] > d:
            pvalue += 1

    return d, pvalue / niter, dis
