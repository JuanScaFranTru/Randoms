from tools import tools
from math import exp
from random import random
import discretes.distributions as dd
import discretes.generics as dg


class Exercise(object):
    def __init__(self):
        name = self.__class__.__name__
        msg = 'Exercise {}'.format(name)
        print()
        print(msg)
        print(len(msg) * '-')


class One(Exercise):
    def __init__(self, n=100, niter=1000):
        super().__init__()
        self.n = n
        self.niter = niter
        self.xs = list(range(1, n + 1))

    def experiment(self):
        perm = dg.random_permutation(self.xs)
        successes = sum([i + 1 == card for i, card in enumerate(perm)])
        return successes

    def run(self):
        results = [self.experiment() for _ in range(self.niter)]
        tools.print_stats(results)


class Two(Exercise):
    def __init__(self, N=10000, niter=100):
        super().__init__()
        self.N = N
        self.niter = niter

        def g(k):
            return exp(k/N)

        self.g = g

    def run(self):
        estimation = dg.monte_carlo_sum(self.g, self.N, self.niter)

        real = dg.monte_carlo_sum(self.g, self.N, self.N)

        error = abs(estimation - real) / real * 100

        print('Estimation: {}'.format(estimation))
        print('Real value: {}'.format(real))
        print('Error: {:2.2f}%'.format(error))


class Three(Exercise):
    MIN_VALUE = 1
    MAX_VALUE = 6

    def __init__(self):
        super().__init__()

    def experiment(self):
        never_occurred = {x: True for x in range(2 * self.MIN_VALUE,
                                                 2 * self.MAX_VALUE + 1)}

        nrolls = 0
        while any(never_occurred.values()):
            U = dd.uniform(self.MIN_VALUE, self.MAX_VALUE)
            V = dd.uniform(self.MIN_VALUE, self.MAX_VALUE)
            X = U + V
            never_occurred[X] = False
            nrolls += 1

        return nrolls

    def run_experiments(self, niter):
        results = [self.experiment() for _ in range(niter)]
        print('Number of iterations: {}'.format(niter))
        tools.print_stats(results)
        print()

    def run(self):
        for niter in [100, 1000, 10000]:
            self.run_experiments(niter)


class FourA(Exercise):
    def __init__(self, lambda_=20, k=18):
        self.lambda_ = lambda_
        self.k = k
        super().__init__()

    def experiment(self):
        while True:
            X = dd.poisson(self.lambda_)
            if X < self.k:
                break
        return X

    def run(self, niter=10000):
        results = [self.experiment() for _ in range(niter)]
        tools.print_stats(results)


class FourB(Exercise):
    def __init__(self, lambda_=20, k=18):
        super().__init__()
        self.lambda_ = lambda_
        self.k = k
        _, self.c = dd.poisson_accum(lambda_, k)

    def experiment(self):
        lambda_ = self.lambda_

        U = random() * self.c
        value = 0
        F = prob = exp(-lambda_)
        while U > F:
            value += 1
            prob *= (lambda_ / value)
            F += prob
        return value - 1

    def run(self, niter=10000):
        results = [self.experiment() for _ in range(niter)]
        tools.print_stats(results)


class Five(Exercise):
    def __init__(self):
        super().__init__()

    def experiment(self):
        def Y_random():
            return dd.geometric(1/3)

        while True:
            Y = Y_random()
            U = random()
            if U < 4/5 * (3/4) ** Y + 2/5:
                break
        return Y

    def run(self, niter=10000):
        results = [self.experiment() for _ in range(niter)]
        tools.print_stats(results)
        tools.plot(lambda: self.experiment(), niter)


if __name__ == '__main__':
    One().run()
    Two().run()
    Three().run()
    FourA().run()
    FourB().run()
    Five().run()
