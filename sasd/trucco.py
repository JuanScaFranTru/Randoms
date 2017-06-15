from continuous.distributions import normal

from math import sqrt, exp
from random import random, uniform
from sasd import generics as g
from numpy import mean
from numpy import var as variance


def print_stats(mean, var, j, n, dev, interval=None):
    print("n: {} >= {}".format(j, n))
    print("Mean: {:2.3f}".format(mean))
    print("Var: {:2.3f}".format(var))
    print("sqrt(var / n): {} < {}".format(sqrt(var / j), dev))
    if interval is not None:
        print("confidence interval: [{:2.3f}, {:2.3f}]".format(*interval))
        a, b = interval
        print("interval length: {:2.3f}".format(b - a))
        print("delta: {:2.3f}".format((b - a)/2))


class Exercise(object):
    def __init__(self):
        name = self.__class__.__name__
        msg = 'Exercise {}'.format(name)
        print()
        print(msg)
        print(len(msg) * '-')


class One(Exercise):
    def run(self, n=30, dev=0.1):

        def generator(): return normal(0, 1)

        mean, var, j = g.estimation(generator, n, dev)
        print_stats(mean, var, j, n, dev)


class Two(Exercise):
    def run(self, n=100, dev=0.01):
        def generator(): return exp(random() ** 2)
        mean, var, j = g.estimation(generator, n, dev)
        print_stats(mean, var, j, n, dev)


class Three(Exercise):
    def run(self, niter=1000, conf=0.95):
        dev = float('inf')

        def generator():
            n = 0
            s = 0
            while s < 1:
                n += 1
                s += random()
            return n

        mean, var, j = g.estimation(generator, niter)

        interval = g.conf_inter(mean, var, j, conf)
        print_stats(mean, var, j, niter, dev, interval)


class Four(Exercise):
    def run(self, niter=1000, conf=0.95):
        dev = float('inf')

        def generator():
            n = 1
            U = random()
            while True:
                n += 1
                V = random()
                if U > V:
                    break
                U = V
            return n

        mean, var, j = g.estimation(generator, niter)

        interval = g.conf_inter(mean, var, j, conf)
        print_stats(mean, var, j, niter, dev, interval)


class Five(Exercise):
    def run(self, niter=1000, L=0.1, conf=0.95):
        def generator():
            X = uniform(-1, 1)
            Y = uniform(-1, 1)
            if sqrt(X ** 2 + Y ** 2) <= 1:
                return 1
            return 0

        dev = g.desv_from_L(L, conf) / 4
        p, var, j = g.estimation_proportion(generator, niter, dev)
        p = 4 * p
        var = var * 16

        interval = g.conf_inter(p, var, j, conf)
        print_stats(p, var, j, niter, dev * 4, interval)


def discrete_uniform(m, k):
    """Uniformly distributed discrete random number in [m, k]."""
    U = random()
    return int(U * (k - m + 1)) + m


def choice(data):
    return data[discrete_uniform(0, len(data) - 1)]


class Six(Exercise):
    def run(self, niter=1000, a=-5, b=5):
        data = [56, 101, 78, 67, 93, 87, 64, 72, 80, 69]
        n = len(data)
        mu = mean(data)  # Empirical mean
        p = 0
        for _ in range(niter):
            random_sample = [choice(data) for _ in range(n)]
            if a < mean(random_sample) - mu < b:
                p += 1
        p /= niter

        print("p = {:2.3f}".format(p))


class Seven(Exercise):
    def exact_bootstrap(data):
        empirical_var = variance(data)
        n = len(data)
        var = 0
        for i in data:
            for j in data:
                var += (variance([i, j], ddof=1) - empirical_var) ** 2
        return var / n ** n

    def run(self, niter=10):
        data = [1, 3]
        var = Seven.exact_bootstrap(data)
        print("exact var = {:2.3f}".format(var))

        var = g.bootstrap(data, variance, lambda x: variance(x, ddof=1), niter)
        print("approx var = {:2.3f}".format(var))


if __name__ == '__main__':
    for cls in [One, Two, Three, Four, Five, Six, Seven]:
        cls().run()
