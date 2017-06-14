from collections import Counter as Freq
from collections import defaultdict
from scipy.stats import chi2


def is_rejected(pvalue, alpha):
    """Is the hypothesis rejected given alpha and pvalue?"""
    return pvalue <= alpha


def chi2_test(p, sample):
    """Return the chi squared statistic and its pvalue

    :param p: hypothesized probability distribution
    :param sample: sample

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
