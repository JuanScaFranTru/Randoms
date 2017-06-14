from random import random


def kolmogorov_d(sample, F):
    sample.sort()
    n = len(sample)
    accum = [F(s) for s in sample]
    diff1 = [(j + 1) / n - a for j, a in enumerate(accum)]
    diff2 = [a - j / n for j, a in enumerate(accum)]
    d = max(diff1 + diff2)
    return d


def kolmogorov_test(sample, F, niter):
    """Return the kolmogorov-Smirnov statistic, its pvalue and its dis.

    Example:
    >>> def F(x): return 1 - exp(- x / 100)
    >>> sample = [66, 72, 81, 94, 112, 116, 124, 140, 145, 155]
    >>> d, pvalue, dis = kolmorogorov_test(sample, F, 500)

    """
    n = len(sample)
    d = kolmogorov_d(sample, F)

    pvalue = 0
    for i in range(niter):
        uniforms = sorted([random() for _ in range(n)])
        uni_diff1 = [(j + 1) / n - u for j, u in enumerate(uniforms)]
        uni_diff2 = [u - j / n for j, u in enumerate(uniforms)]
        dis = max(uni_diff1 + uni_diff2)
        if dis > d:
            pvalue += 1

    return d, pvalue / niter
