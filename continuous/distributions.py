from math import log, sqrt, cos, sin, pi
from random import random


def uniform(a, b):
    """Get a random number in [a, b]."""
    return (b - a) * random() + a


def nroot(n):
    """Generate a random number with CDF F(x) = x ** n.

    This function uses the fact that the CDF of the max of n uniformly
    distributed random variables is: F(x) = x ** n.
    """
    return max([random() for _ in range(n)])


def nroot2(n):
    """Generate a random number with CDF F(x) = x ** n.

    This function uses the acceptance-rejection method.
    The PDF is: f(x) = n * x ** (n - 1)
    The g function is: g(x) = 1
    The h function is: h(x) = n * x ** (n - 1) and c is equal to n.
    """
    Y = random()
    U = random()
    while U >= Y ** (n - 1):
        U = random()
        Y = random()
    return Y


def nroot3(n):
    """Generate a random number with CDF F(x) = x ** n.

    This function uses the inverse transform method.
    """
    return random() ** (1 / n)


def exponential(lambda_):
    """Exponential distribution."""
    U = random()
    return (-log(1 - U)) / lambda_


def gamma(n, lambda_):
    """Gamma distrubution.

    This function uses the fact that the sum of n exponential random variables
    with parameter lambda is a Gamma random variable.
    """
    U = 1
    for _ in range(n):
        U *= random()
    return (-log(U)) / lambda_


def nExponentials(n, lambda_):
    """Get n exponentially distributed random numbers."""
    t = gamma(n, lambda_)

    Us = [random() for _ in range(n - 1)] + [0, 1]

    Us.sort()

    return [t * (Us[i + 1] - Us[i]) for i in range(n)]


def normal(mu, sigma):
    """Normal distribution."""
    while True:
        Y1 = exponential(1)
        Y2 = exponential(1)
        if Y2 >= (Y1 - 1) ** 2 / 2:
            break

    if random() < 0.5:
        return Y1 * sigma + mu
    else:
        return -Y1 * sigma + mu


def twonormal(mu, sigma):
    """Return two normal distributed random variables."""
    rcuad = exponential(1/2)
    theta = uniform(0, 2 * pi)

    tmp = sqrt(rcuad)
    return tmp * cos(theta), tmp * sin(theta)


def twonormal2(mu, sigma):
    """Return two normal distributed random variables."""
    while True:
        V1, V2 = uniform(-1, 1), uniform(-1, 1)
        S = V1 ** 2 + V2 ** 2
        if S <= 1:
            break

    tmp = sqrt(-2 * log(S) / S)
    return V1 * tmp, V2 * tmp
