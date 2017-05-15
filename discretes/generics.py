from numpy import mean
from numpy import var
from random import random


def print_stats(xs):
    """Print mean and variance of xs in stdout."""
    template = "Mean: {:2.2f} \t Variance: {:2.2f}"
    print(template.format(mean(xs), var(xs)))


def inverse_transform(ps, xs):
    """Get a random value given a discrete distribution.

    ps -- ps[i] is the probability of x[i].
    xs -- list of possible values of the random variable.
    """
    U = random()
    i = 0
    F = ps[0]
    while U >= F:
        i += 1
        F += ps[i]
    return xs[i]


def sort_by_probability(ps, xs):
    """Sort ps and xs by highest probability.

    ps -- ps[i] is the probability of xs[i].
    x -- list of possible values of the random variable.
    return -- a tuple with sorted ps and xs.
    """
    sorted_list_of_tuples = sorted(zip(ps, xs), reverse=True)
    ps, xs = zip(*sorted_list_of_tuples)
    ps, xs = list(ps), list(xs)
    return ps, xs


def accept_and_reject(Y_random, c, ps, q):
    """Get a random number using the accept and reject method.

    Y_random -- a random number generator with the same distribution as Y.
    c -- a constant c such that ps(j)/q(j) <= c for all j in the domain of ps.
    ps -- distribution ps.
    q -- distribution q.
    """
    while True:
        Y = Y_random()
        U = random()
        if U < ps(Y) / (c * q(Y)):
            break
    return Y


def composition(ps, F):
    """Simulate variable X = sum([ps[i]*F[i] for i in range(len(ps))])

    ps -- List of weights. sum(ps[i]) == 1.
    F -- List random number generators with distribution F[i].
    """
    U = random()
    j = 0
    acc = ps[j]
    while U >= acc:
        j += 1
        acc += ps[j]

    return F[j]()


class Alias(object):
    class Bivalued(object):
        def __init__(self, j, i, ps):
            self.j = j
            self.i = i
            self.ps = ps
            self.q = 1 - ps

        def random(self, V):
            if V < self.ps:
                return self.j
            else:
                return self.i

    def __init__(self, ps, xs):
        """Initialize the alias random number generator for distribution ps.

        This method is used when generating random variables with a finite
        number of values, say {1, ..., n}.
        """
        self.n = n = len(list(ps))
        self.Xs = [None] * n
        self.xs = xs

        for i, p in enumerate(ps):
            ps[i] = p * (n - 1)

        for k in range(n - 1):
            positive_p = [x for x in ps if x > 0]

            min_p = min(positive_p)
            j = ps.index(min_p)

            max_p = max(positive_p)
            i = ps.index(max_p)

            self.Xs[k] = self.Bivalued(j, i, min_p)

            ps[j] -= min_p
            ps[i] -= 1 - min_p

    def random(self):
        """Get a random number with distribution ps."""
        I = int(random() * (self.n - 1))
        V = random()
        i = self.Xs[I].random(V)
        return self.xs[i]


def monte_carlo_sum(g, N, niter=100):
    """Aproximate the sum of g(i) for i in the interval [1, N].

    If the number of iterations is not less than N, then the exact sum is
    returned.

    g -- A function with domain of natural numbers.
    N -- The upper limit of the summation.
    niter -- The number of iterations of the algorithm (optional).
    """
    if niter >= N:
        return sum((g(i) for i in range(1, N+1)))

    S = 0
    for i in range(niter):
        j = int(N * random()) + 1
        S += g(j)

    S = S * N / niter
    return S


def random_permutation(xs):
    """Get an equiprobable random permutation of x."""
    N = len(xs)
    for j in reversed(range(N)):
        i = int(j * random())
        xs[j], xs[i] = xs[i], xs[j]
    return xs


def random_subset(r, xs):
    """Get an equiprobable random subset of xs with r elements.

    r -- number of elements in the generated subset
    xs -- set (represented as a list)
    """
    N = len(xs)
    for j in reversed(range(N - r, N)):
        i = int(j * random())
        xs[j], xs[i] = xs[i], xs[j]
    return xs[-r:]
