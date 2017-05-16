from math import log, sqrt, cos, sin, pi, exp
from random import random
from discretes.distributions import poisson


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
    """
    Y = random()
    U = random()
    while U >= Y ** (n - 1):
        U = random()
        Y = random()
    return Y


def exponential(lambda_):
    """Exponential distribution."""
    U = random()
    return (-log(U)) / lambda_


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
    rcuad = exponential(1 / 2)
    theta = uniform(0, 2 * pi)

    tmp = sqrt(rcuad)
    return tmp * cos(theta), tmp * sin(theta)


def twonormal2(mu, sigma):
    """Return two normal distributed random variables."""
    while True:
        U1, U2 = uniform(-1, 1), uniform(-1, 1)
        S = U1 ** 2 + U2 ** 2
        if S <= 1:
            break

    tmp = sqrt(-2 * log(S) / S)
    return U1 * tmp, U2 * tmp


def poisson_N(lambda_):
    """Return the number of events N(1) of a poisson process."""
    n = 0
    prod = random()
    while prod < exp(-lambda_):
        n += 1
        prod *= random()
    return n - 1


def poisson_process(T, lambda_):
    """Generate an homogeneous poisson process.

    T -- Generate until an event occurs after time T.
    lambda_ -- Param of the distribution.
    """
    t = 0.0
    S = []
    while True:
        E = exponential(lambda_)
        if t + E > T:
            break
        t += E
        S.append(t)
    return S


def poisson_process2(T, lambda_):
    """Generate an homogeneous poisson process.

    T -- Generate until an event occurs after time T.
    lambda_ -- Param of the distribution.
    """
    n = poisson(lambda_ * T)
    Us = [uniform(0, T) for _ in range(n)]

    S = [T * U for U in sorted(Us)]

    return S


def non_homogeneous_poisson_process(T, lambda_t, lambda_):
    """Generate a non homogeneous poisson process.

    T -- Generate until an event occurs after time T.
    lambda_t --  λ(t).
    lambda_ -- a upper bound for λ(t).
    """
    t = 0
    S = []
    while True:
        E = exponential(lambda_)
        if t + E > T:
            break
        t += E
        if random() < (lambda_t(t) / lambda_):
            S.append(t)
    return S
