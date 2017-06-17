from random import random
from math import log, sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import iqr


def print_stats(data):
    """Print mean and std dev of data and return the pair (mean, std dev)."""
    template = "mu: {:2.3f} \t sigma: {:2.3f}"
    sigma = sqrt(np.var(data, ddof=1))
    mu = np.mean(data)
    print(template.format(mu, sigma))


def plot_histogram(data, h=None, number=0):
    """Plot a histogram of the distribution X_random.

    data -- data to plot
    f -- PDF (optional)
    title -- title (optional)
    """
    if h is None:
        n = len(data)
        h = 2 * iqr(data) / (n ** (1/3))  # Freedman–Diaconis rule

    nbins = (max(data) - min(data)) / h
    nbins = int(nbins)

    mu, sigma = np.mean(data), sqrt(np.var(data, ddof=1))
    label = "$\mu={:2.3f},\ \sigma={:2.3f}$".format(mu, sigma)

    plt.hist(data, nbins, normed=1, alpha=0.5, edgecolor="w", label=label)
    plt.legend(loc='upper right')
    plt.xlim(0, 10)
    plt.ylim(0, 0.7)
    plt.title("Experiment {}".format(number))
    plt.xlabel('Time to Fail (months)')
    plt.ylabel('Frequency')


def exponential(lambda_):
    """Exponential distribution."""
    U = random()
    return (-log(U)) / lambda_


def simulation(n, spare, Tf, Tg, oper):
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


def run(n=5, spare=2, Tf=1, Tg=0.125, oper=1, niter=10000):
    data = [None] * niter
    for i in range(niter):
        data[i] = simulation(n, spare, Tf, Tg, oper)
    data = np.array(data)
    return data


if __name__ == '__main__':
    es = [run(), run(oper=2), run(spare=3)]

    nbins = 0.1
    j = 0
    for e in es:
        print_stats(e)
        plot_histogram(e, nbins, number=j)
        j += 1
        plt.show()

    for e in es:
        plot_histogram(e, nbins, j)
    j += 1
    plt.show()

    plot_histogram(es[0], nbins, j)
    plot_histogram(es[1], nbins, j)
    j += 1
    plt.show()

    plot_histogram(es[1], nbins, j)
    plot_histogram(es[2], nbins, j)
    j += 1
    plt.show()
