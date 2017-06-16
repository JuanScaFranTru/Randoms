import numpy as np
from numpy import mean, var
import matplotlib.pyplot as plt
from scipy.stats import iqr


def print_stats(xs):
    """Print mean and variance of xs in stdout."""
    template = "Mean: {:2.2f} \t Variance: {:2.2f}"
    print(template.format(mean(xs), var(xs)))


def plotcurve(f, n, a, b):
    xs = np.arange(a, b, (b-a)/n)
    ys = [f(x) for x in xs]
    plt.plot(xs, ys)


def plot_histogram(values, filename=None, title=None):
    """Plot a histogram of the distribution X_random.

    values -- values to plot
    f -- PDF (optional)
    title -- title (optional)
    """
    xs = values
    n = len(xs)
    h = 2 * iqr(xs) / (n ** (1/3))  # Freedman–Diaconis rule
    if h == 0:
        nbins = 1000
    else:
        nbins = (max(xs) - min(xs)) / h
        nbins = int(nbins)

    xs_set = set(xs)
    if len(xs_set) < 20:
        nbins = len(xs_set)

    if filename is not None:
        plotcurve(filename, len(xs_set), min(xs_set), max(xs_set))

    plt.hist(xs, nbins, normed=1)
    plt.title(title)
    plt.xlabel('Time to Fail (months)')
    plt.ylabel('Frequency')
    plt.show()
