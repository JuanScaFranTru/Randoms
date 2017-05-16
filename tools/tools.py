from numpy import mean
from numpy import var

import discretes.distributions as dd
import matplotlib.pyplot as plt
from scipy.stats import iqr
import numpy as np


def print_stats(xs):
    """Print mean and variance of xs in stdout."""
    template = "Mean: {:2.2f} \t Variance: {:2.2f}"
    print(template.format(mean(xs), var(xs)))


def plotcurve(f, n, a, b):
    xs = np.arange(a, b, (b-a)/n)
    ys = [f(x) for x in xs]
    plt.plot(xs, ys)


def plot_histogram(xs, nbins, title=None):
    """Plot a histogram of xs"""
    if title is None:
        title = 'Histogram'

    plt.hist(xs, nbins, normed=1)
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()


def plot(X_random, nsamples=1000, f=None, title=None):
    """Plot a histogram of the distribution X_random.

    X_random -- random number generator.
    nsamples -- number of samples (optional)
    f -- PDF (optional)
    title -- title (optional)
    """
    xs = [X_random() for _ in range(nsamples)]
    n = len(xs)
    h = 2 * iqr(xs) / (n ** (1/3))  # Freedman–Diaconis rule
    nbins = (max(xs) - min(xs)) / h
    nbins = int(nbins)

    xs_set = set(xs)
    if len(xs_set) < 20:
        nbins = len(xs_set)

    if f is not None:
        plotcurve(f, len(xs_set), min(xs_set), max(xs_set))

    plot_histogram(xs, nbins, title)


if __name__ == '__main__':
    plot(lambda: dd.geometric(0.1), 100000, 'geometric')
    plot(lambda: dd.uniform(0, 1000), 100000, 'uniform')
    plot(lambda: dd.binomial(10, 0.5), 100000, 'binomial')
    plot(lambda: dd.bernoulli(0.5), 100000, 'bernoulli')
    plot(lambda: dd.poisson(100), 100000, 'poisson')
