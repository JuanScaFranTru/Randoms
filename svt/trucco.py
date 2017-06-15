from random import random
from numpy import mean, var
from math import exp, log, sqrt
from collections import Counter as Freq
import scipy.stats as st
import svt.chi2 as c
import svt.kolmogorov as k
import svt.twosamples as ts
from continuous.distributions import normal


def ncr(n, r):
    r = min(r, n-r)
    if r == 0:
        return 1
    numer = 1
    for i in range(n, n - r, -1):
        numer *= i

    denom = 1
    for i in range(1, r + 1):
        denom *= i

    return numer // denom


class Exercise(object):
    def __init__(self):
        name = self.__class__.__name__
        msg = 'Exercise {}'.format(name)
        print()
        print(msg)
        print(len(msg) * '-')


class One(Exercise):
    def run(self, niter=100):
        sample = list(Freq({0: 141, 1: 291, 2: 132}).elements())

        p = {
            0: 1/4,  # Blancas
            1: 1/2,  # Rosas
            2: 1/4,  # Rojas
        }

        t, pvalue = c.chi2_test(sample, p)
        print("t: {:2.5f} p-value: {:2.5f}".format(t, pvalue))

        t, pvalue = c.chi2_test_simulate(sample, p, niter)
        print("t: {:2.5f} p-value: {:2.5f}".format(t, pvalue))


class Two(Exercise):
    def run(self, niter=100):
        sample = list(Freq({0: 158,
                            1: 172,
                            2: 164,
                            3: 181,
                            4: 160,
                            5: 165}).elements())

        p = {i: 1/6 for i in range(6)}

        t, pvalue = c.chi2_test(sample, p)
        print("t: {:2.5f} p-value: {:2.5f}".format(t, pvalue))

        t, pvalue = c.chi2_test_simulate(sample, p, niter)
        print("t: {:2.5f} p-value: {:2.5f}".format(t, pvalue))


class Three(Exercise):
    def run(self, niter=1000):

        def F(x):
            if x > 1:
                return 1
            elif x < 0:
                return 0
            else:
                return x

        sample = [0.12, 0.18, 0.06, 0.33, 0.72, 0.83, 0.36, 0.27, 0.77, 0.74]
        d, pvalue = k.kolmogorov_test(sample, F, niter)
        print("d: {:2.5f} p-value: {:2.5f}".format(d, pvalue))


class Four(Exercise):
    def run(self, niter=1000):
        def F(x): return 1 - exp(- x / 50)
        sample = [86, 133, 75, 22, 11, 144, 78, 122, 8, 146, 33, 41, 99]
        d, pvalue = k.kolmogorov_test(sample, F, niter)
        print("d: {:2.5f} p-value: {:2.5f}".format(d, pvalue))


class Five(Exercise):
    def run(self, niter=1000):
        s = [6, 7, 3, 4, 7, 3, 7, 2, 6, 3, 7, 8, 2, 1, 3, 5, 8, 7]

        def estimate(sample):
            n = 8
            prob = mean(sample) / n
            p = {i: ncr(n, i) * prob ** i * (1 - prob) ** (n - i)
                 for i in range(n - 1)}

            p[n - 1] = 1 - sum(p.values())
            return p

        p = estimate(s)

        def generator(): return c.inverse_transform(p)

        t, pvalue = c.chi2_test(s, p, 1)
        print("d: {:2.5f} p-value: {:2.5f}".format(t, pvalue))

        t, pvalue = c.chi2_test_unk_params(len(s), t, estimate,
                                           generator, niter)
        print("d: {:2.5f} p-value: {:2.5f}".format(t, pvalue))


class Six(Exercise):
    def exponential():
        return (-log(random()))

    def run(self, niter=1000):
        sample = [Six.exponential() for i in range(10)]

        def F(x): return 1 - exp(-x)
        d, pvalue = k.kolmogorov_test(sample, F, niter)
        print("d: {:2.5f} p-value: {:2.5f}".format(d, pvalue))


class Seven(Exercise):
    def run(self, niter=1000):
        s = [1.6, 10.3, 3.5, 13.5, 18.4, 7.7, 24.3, 10.7,
             8.4, 4.9, 7.9, 12, 16.2, 6.8, 14.7]

        def estimate(sample, lam=None):
            if lam is None:
                lam = 1 / mean(sample)

            def F(x):
                return 1 - exp(-lam * x)
            return F

        def generator(lam): return lambda: (-log(random())) / lam

        lam = 1 / mean(s)
        F = estimate(s)
        d = k.kolmogorov_d(s, F)

        d, pvalue = k.kolmogorov_test_unk_params(len(s), d, estimate,
                                                 generator(lam), niter)
        print("d: {:2.5f} p-value: {:2.5f}".format(d, pvalue))


class Eight(Exercise):
    def run(self, niter=1000):
        s = [91.9, 97.8, 111.4, 122.3, 105.4, 95.0,
             103.8, 99.6, 96.6, 119.3, 104.8, 101.7]

        def estimate(sample, mu=None, sigma=None):
            if mu is None:
                mu = mean(sample)
            if sigma is None:
                sigma = sqrt(var(sample, ddof=1))

            def F(x):
                return st.norm.cdf((x - mu) / sigma)

            return F

        def generator(mu, sigma):
            return lambda: normal(mu, sigma)

        mu = mean(s)
        sigma = sqrt(var(s, ddof=1))
        F = estimate(s, mu, sigma)

        d, pvalue = k.kolmogorov_test(s, F, niter)
        print("d: {:2.5f} p-value: {:2.5f}".format(d, pvalue))

        d, pvalue = k.kolmogorov_test_unk_params(len(s), d, estimate,
                                                 generator(mu, sigma), niter)
        print("d: {:2.5f} p-value: {:2.5f}".format(d, pvalue))


class Nine(Exercise):
    def run(self, niter=1000):
        sample1 = [65.2, 67.1, 69.4, 78.4, 74.0, 80.3]
        sample2 = [59.4, 72.1, 68.0, 66.2, 58.5]

        pvalue = ts.two_samples_small(sample1, sample2)
        print("exact p-value: {:2.5f}".format(pvalue))

        pvalue = ts.two_samples_normal(sample1, sample2)
        print("p-value approx with normal: {:2.5f}".format(pvalue))

        pvalue = ts.two_samples_sim(sample1, sample2, niter)
        print("p-value simulated: {:2.5f}".format(pvalue))


class Ten(Exercise):
    def run(self, niter=1000):
        sample1 = [19, 31, 39, 45, 47, 66, 75]
        sample2 = [28, 36, 44, 49, 52, 72, 72]

        pvalue = ts.two_samples_small(sample1, sample2)
        print("exact p-value: {:2.5f}".format(pvalue))

        pvalue = ts.two_samples_normal(sample1, sample2)
        print("p-value approx with normal: {:2.5f}".format(pvalue))

        pvalue = ts.two_samples_sim(sample1, sample2, niter)
        print("p-value simulated: {:2.5f}".format(pvalue))


if __name__ == '__main__':
    for cls in [One, Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten]:
        cls().run()
