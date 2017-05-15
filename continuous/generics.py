from random import random


def inverse_transform(G):
    """Generate a random number using the inverse CDF G."""
    return G(random())


def rejection(Y_random, c, f, g):
    """Get a random number using the acceptance-rejection method.

    Y_random -- a random number generator with the same distribution as Y.
    c -- a constant c such that ps(j)/q(j) <= c for all j in the domain of ps.
    ps -- distribution ps.
    q -- distribution q.
    """
    while True:
        Y = Y_random()
        U = random()
        if U < f(Y) / (c * g(Y)):
            break
    return Y


def composition(ps, Fs):
    """Simulate variable X = sum([p * F() for p, F in zip(ps, Fs)])

    ps -- List of weights. sum(ps) == 1.
    F -- List random number generators.
    """
    U = random()
    j = 0
    acc = ps[j]
    while U >= acc:
        j += 1
        acc += ps[j]

    return Fs[j]()
