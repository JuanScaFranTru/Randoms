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
    """Return the kolmogorov-Smirnov statistic and its pvalue.

    Example:
    >>> def F(x): return 1 - exp(- x / 100)
    >>> sample = [66, 72, 81, 94, 112, 116, 124, 140, 145, 155]
    >>> d, pvalue = kolmogorov_test(sample, F, 500)

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


def kolmogorov_test_unk_params(n, d, estimate_F, generator, niter):
    """
    >>> def estimate(sample, lam=None):
    >>>     if lam is None:
    >>>         lam = 1 / mean(sample)
    >>>     def F(x):
    >>>         return 1 - exp(-lam * x)
    >>>     return F
    >>> def generator(lam): return lambda: (-log(random())) / lam
    >>> sample = [1.6, 10.3, 3.5, 13.5, 18.4, 7.7, 24.3, 10.7,
    >>>           8.4, 4.9, 7.9, 12, 16.2, 6.8, 14.7]
    >>> lam = 1/mean(sample)
    >>> n = len(sample)
    >>> F = estimate(sample)
    >>> d = kolmogorov_d(sample, F)
    >>> print(kolmogorov_test(sample, F, 1))
    >>> print(kolmogorov_test_unk_params(n, d, estimate, generator(lam), 1000))
    """
    pvalue = 0
    for i in range(niter):
        generated_sample = [generator() for _ in range(n)]
        F_sim = estimate_F(generated_sample)
        di = kolmogorov_d(generated_sample, F_sim)
        if di >= d:
            pvalue += 1
    return d, pvalue / niter
