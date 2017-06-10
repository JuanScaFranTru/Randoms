from math import sqrt
from scipy import stats as st


def simulate(generator, n, desv=float('inf')):
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
