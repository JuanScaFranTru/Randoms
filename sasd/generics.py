from math import sqrt
from scipy import stats as st
from random import choice


def estimation_proportion(generator, n, dev=float('inf')):
    """Estimates p using the recursive form for mean and variance.

    :param generator: random number generator
    :param n: number of iterations
    :param dev: minimum standard deviation

    :return: 3-uple of the form (p, var, j)
    """
    p = 0
    j = 0
    while j < n or sqrt((1 - p) * p / j) > dev:
        j += 1
        x = generator()
        p = p + 1 / j * (x - p)

    return p, (1 - p) * p, j


def estimation(generator, n, dev=float('inf')):
    """Estimate mean using the recursive form for mean and variance.

    :param generator: random number generator
    :param n: number of iterations
    :param dev: minimum standard deviation

    :return: 3-uple of the form (mean, var, j)
    """
    mean = 0
    var = 0
    j = 0
    while j < n or sqrt(var / j) > dev:
        j += 1
        x = generator()
        old_mean = mean
        mean = mean + 1 / j * (x - mean)
        if var != 0:
            var *= (1 - 1/(j - 1))
        var += j * (mean - old_mean) ** 2

    return mean, var, j


def zeta(alpha):
    return st.norm.ppf(1 - alpha)


def desv_from_L(L, conf):
    alpha = 1 - conf
    return L / (2 * zeta(alpha / 2))


def conf_inter(mean, var, n, conf):
    """Return confidence interval for mean estimation.

    :param mean: mean
    :param var: variance
    :param n: sample size
    :param conf: confidence of the interval (from 0 to 1)

    :return: confidence interval in the form of a pair
    """
    alpha = 1 - conf
    z = zeta(alpha / 2)
    delta = z * sqrt(var / n)
    return (mean - delta, mean + delta)


def bootstrap(data, param, estimator, niter):
    """Return the ECM of estimator

    :param data: Data
    :param param: Parameter evaluated in the empirical distribution of the data
    :param estimator: Parameter estimator
    :param niter: Number of iterations of the Monte Carlo approximation

    :return: Mean Squared Error (MSE)

    Examples of usage:
        >>> from numpy import mean, var
        >>> data = [1, 2, 3, 4]
        >>> bootstrap(data, mean, mean, 1000)
        >>> bootstrap(data, var, lambda x: var(x, ddof=1), 1000)
    """
    n = len(data)
    ecm = 0
    for _ in range(niter):
        sample = [choice(data) for _ in range(n)]
        ecm += (estimator(sample) - param(data)) ** 2
    return ecm / niter
