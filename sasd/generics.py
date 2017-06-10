from math import sqrt
from scipy import stats as st


def estimation(generator, n, desv=float('inf')):
    """Estimates mean using the recursive form for mean and variance.
    Also return the variance estimator and number of iterations for the
    estimation.

    :param n: min number of iterations to the estimation
    :param dist: distribution probability function for the random variable
                that we
    :param want to estimate the mean.
    :param accept_value: acceptable value for variance. [default: None]

    :return 3-uple with the form (mean, var, data_len)
    """
    mean = 0
    var = 0
    j = 0
    while j < n or sqrt(var / j) > desv:
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
    mean: mean estimation

    :param var: variance (estimation or not) that will be used to compute the
                interval
    :param n: data_len (number of samples)
    :param conf: confidence for acceptance (z_(α/2))

    :return confidence for acceptance interval
    """
    alpha = 1 - conf
    z = zeta(alpha / 2)
    delta = z * sqrt(var / n)
    return (mean - delta, mean + delta)
