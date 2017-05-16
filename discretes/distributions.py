from random import random
from math import log
from math import exp


def uniform(m, k):
    """Uniformly distributed discrete random number in [m, k]."""
    U = random()
    return int(U * (k - m + 1)) + m


def geometric(p):
    """Geometric distribution."""
    return int(log(random()) / log(1 - p)) + 1


def bernoulli(p):
    """Bernoulli distribution."""
    U = random()

    if U < p:
        return 1
    else:
        return 0


def bernoulli_batch(p, N):
    """Get N Bernoulli distributed random numbers."""

    result = [0] * N

    M = 0
    while True:
        B = geometric(p)
        M += B
        if M - 1 >= N:
            break
        result[M - 1] = 1

    return result


def poisson_accum(lam, j):
    prob = exp(-lam)
    F = prob
    for i in range(1, j + 1):
        prob *= (lam / i)
        F += prob
    return prob, F


def poisson(lam):
    """Poisson distribution."""
    value = int(lam)
    prob, F = poisson_accum(lam, value)
    u = random()
    if u >= F:
        while u >= F:
            value += 1
            prob *= lam / value
            F += prob
        return value - 1
    else:
        while u < F:
            F -= prob
            prob *= value / lam
            value -= 1
        return max(value, 0)


def binomial(n, p):
    """Binomial distribution."""

    U = random()
    i = 0
    q = 1 - p
    F = prob = (q) ** n

    while U >= F:
        prob = p / q * (n - i) / (i + 1) * prob
        F += prob
        i += 1
    return i
