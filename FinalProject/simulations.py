from random import random
from math import log, sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import iqr


def print_stats(data):
    """Print mean and std dev of data and return the pair (mean, std dev)."""
    template = "Mean: {:2.2f} \t Variance: {:2.2f}"
    sigma = sqrt(np.var(data, ddof=1))
    mu = np.mean(data)
    print(template.format(mu, sigma))
    return mu, sigma


def plot_histogram(data, title=None):
    """Plot a histogram of the distribution X_random.

    data -- data to plot
    f -- PDF (optional)
    title -- title (optional)
    """
    n = len(data)
    h = 2 * iqr(data) / (n ** (1/3))  # Freedman–Diaconis rule
    if h == 0:
        nbins = 1000
    else:
        nbins = (max(data) - min(data)) / h
        nbins = int(nbins)

    plt.hist(data, nbins, normed=1)
    plt.title(title)
    plt.xlabel('Time to Fail (months)')
    plt.ylabel('Frequency')
    plt.show()


def exponential(lambda_):
    """Exponential distribution."""
    U = random()
    return (-log(U)) / lambda_


def simulation1(n, spare, Tf, Tg):
    assert n > 0
    assert spare >= 0

    def random_fail(): return exponential(1 / Tf)

    def random_fix(): return exponential(1 / Tg)

    inf = float('inf')
    fails = [random_fail() for i in range(n)]
    fails.sort()
    t = 0
    broken = 0
    t_fixed = inf

    while True:
        if fails[0] < t_fixed:
            t = fails[0]
            broken += 1
            if broken >= spare + 1:
                return t
            if broken < spare + 1:
                fails[0] = t + random_fail()
                fails.sort()
            if broken == 1:
                t_fixed = t + random_fix()
        else:
            t = t_fixed
            broken -= 1
            if broken > 0:
                t_fixed = t + random_fix()
            if broken == 0:
                t_fixed = inf


def simulation2(n, spare, Tf, Tg, oper):
    assert n > 0
    assert spare >= 0

    def random_fail(): return exponential(1 / Tf)

    def random_fix(): return exponential(1 / Tg)

    inf = float('inf')
    fails = [random_fail() for i in range(n)]
    fails.sort()
    t = 0
    broken = 0
    fixing = 0
    # Dos operarios
    t_fixed = [inf] * oper

    while True:
        # Se rompe una antes de que alguno de los dos operarios termine de
        # arreglar
        if fails[0] < t_fixed[oper - 1]:
            t = fails[0]
            broken += 1
            if broken >= spare + 1:
                return t
            if broken < spare + 1:
                fails[0] = t + random_fail()
                fails.sort()

            i = 0
            while broken > fixing and t_fixed[i] == inf:
                t_fixed[i] = t + random_fix()
                fixing += 1
                i += 1
            t_fixed.sort(reverse=True)

        else:
            t = t_fixed[oper - 1]
            broken -= 1
            fixing -= 1

            if broken > fixing:
                t_fixed[oper - 1] = t + random_fix()
                fixing += 1
            if broken == fixing:
                t_fixed[oper - 1] = inf
            t_fixed.sort(reverse=True)


if __name__ == '__main__':
    n = 5
    spare = 2
    Tf = 1
    Tg = 0.125
    niter = 10000
    oper = 2

    data = [None] * niter
    for i in range(niter):
        data[i] = simulation1(n, spare, Tf, Tg)

    mu, sigma = print_stats(data)
    plot_histogram(data)

    for i in range(niter):
        data[i] = simulation2(n, spare, Tf, Tg, oper)

    mu, sigma = print_stats(data)
    plot_histogram(data)
