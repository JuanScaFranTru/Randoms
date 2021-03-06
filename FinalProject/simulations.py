from random import random
from math import log, sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import iqr


def print_stats(data):
    """Print mean and std dev of data and return the pair (mean, std dev)."""
    template = "**mu**: {:2.3f} \t **sigma**: {:2.3f}"
    sigma = sqrt(np.var(data, ddof=1))
    mu = np.mean(data)
    print(template.format(mu, sigma))


def plot_histogram(data, h, title=None, label=None):
    """Plot a histogram of the distribution X_random.

    data -- data to plot
    f -- PDF (optional)
    title -- title (optional)
    """
    bins = np.linspace(0, 20, 60)
    mu, sigma = np.mean(data), sqrt(np.var(data, ddof=1))
    label = label + "$\mu={:2.3f},\ \sigma={:2.3f}$".format(mu, sigma)

    data = np.array(data)
    plt.hist(data, weights=np.zeros_like(data) + 1. / data.size, bins=bins,
             alpha=0.5, edgecolor="w", label=label)
    plt.legend(loc='upper right')
    plt.xlim(0, 15)

    plt.title(title)
    plt.xlabel('Tiempo de falla (meses)')
    plt.ylabel('Frecuencia')


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

            if broken == fixing:
                t_fixed[oper - 1] = inf
            if broken > fixing:
                t_fixed[oper - 1] = t + random_fix()
                fixing += 1
            t_fixed.sort(reverse=True)


def run(n=5, spare=2, Tf=1, Tg=0.125, oper=1, niter=10000):
    data = [None] * niter
    for i in range(niter):
        data[i] = simulation(n, spare, Tf, Tg, oper)
    data = np.array(data)
    return data


def comparison(es):
    h = 0.5
    title = ''
    plt.figure(num=None, figsize=(8, 6), dpi=150, facecolor='w', edgecolor='k')
    for i, v in enumerate(es.items()):
        if i > 0:
            title += 'vs. '
        param, e = v
        label = 'S={}, O={} '.format(*param)
        title += label
        plot_histogram(e, h, title, label)
    plt.savefig('../report/images/' + title.replace('.', '')
                                 .replace(' ', '')
                                 .replace(',', '')
                                 .replace('=', ''))
    plt.show()


if __name__ == '__main__':
    params = [(2, 1), (2, 2), (3, 1)]  # (spare, oper)
    es = {(s, o): run(spare=s, oper=o) for s, o in params}

    comparison({params[i]: es[params[i]] for i in [0, 2]})
    comparison({params[i]: es[params[i]] for i in [0, 1]})
    comparison({params[i]: es[params[i]] for i in [1, 2]})
