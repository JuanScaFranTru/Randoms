from collections import Counter as Freq
from collections import defaultdict
from scipy.stats import chi2


def is_rejected(pvalue, alpha):
    """Is the hypothesis rejected given alpha and pvalue?"""
    return pvalue <= alpha


def chi2_t(sample, p):
    a, b = min(p), max(p)
    p = defaultdict(float, p)
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
