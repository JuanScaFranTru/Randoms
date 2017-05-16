from tools import tools
from math import exp, sqrt, log
from random import random

from tabulate import tabulate
import continuous.distributions as cd
import continuous.generics as cg
import discretes.distributions as dd


class Exercise(object):
    def __init__(self, name, niter=100000, f=None):
        self.niter = niter
        self.name = name
        self.f = f
        msg = 'Exercise {}'.format(name)
        print()
        print(msg)
        print(len(msg) * '-')

    def run(self, plot=False):
        results = [self.experiment() for _ in range(self.niter)]
        tools.print_stats(results)

        if plot and self.f is None:
            tools.plot(self.experiment, self.niter)

        if plot and self.f is not None:
            tools.plot(self.experiment, self.niter, f=self.f)


class One(Exercise):
    def __init__(self):
        def G(x):
            if x < 1/4:
                return 2 * sqrt(x) + 2
            else:
                return 6 - 6 * sqrt(1 - 1/3 * (2 + x))
        self.G = G

        def f(x):
            if x >= 2 and x <= 3:
                return x / 2 - 1
            if x >= 3 and x <= 6:
                return 1 - x / 6
            return 0
        super().__init__('One', f=f)

    def experiment(self):
        return self.G(random())


class Two(Exercise):
    def __init__(self, alpha=1, beta=1):
        self.alpha = a = alpha
        self.beta = b = beta

        def G(x):
            return (log(1-x)/(-a)) ** (1/b)
        self.G = G

        def f(x):
            a = self.alpha
            b = self.beta
            return a * b * x ** (b - 1) * exp(-a * x ** b)
        super().__init__('Two', f=f)

    def experiment(self):
        return self.G(random())


class Four(Exercise):
    def __init__(self):
        super().__init__('Four')

    def experiment(self):
        Y = cd.exponential(1)
        return cd.nroot2(Y)


class SevenA(Exercise):
    def __init__(self):
        def f(x):
            return x * exp(-x)
        super().__init__('Seven A', f=f)

    def experiment(self):
        return cd.gamma(2, 1)


class SevenB(Exercise):
    def __init__(self):
        self.c = 2

        def Y_random(): return (-log(random())) * 2
        self.Y_random = Y_random

        def g(Y): return 1/2 * exp(-1/2 * Y)
        self.g = g

        def f(x):
            return x * exp(-x)
        super().__init__('Seven B', f=f)

    def experiment(self):
        return cg.rejection(self.Y_random, self.c, self.f, self.g)


class Eleven(Exercise):
    def __init__(self, lambda_=5, T=1, min_capacity=20, max_capacity=40):
        super().__init__('Eleven')
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity
        self.lambda_ = lambda_
        self.T = T

    def experiment(self):
        return cd.poisson_process(self.T, self.lambda_)

    def run(self):
        events = self.experiment()
        a = self.min_capacity
        b = self.max_capacity
        fans = [[event, dd.uniform(a, b)] for event in events]

        t = tabulate(fans, ['Time of arrival', 'Fans'], tablefmt='fancy_grid')
        print()
        print(t)


class Twelve(Exercise):
    def __init__(self, T=10):
        super().__init__('Twelve')

        def lambda_t(t):
            return 3 + 4 / (t+1)

        self.lambda_t = lambda_t
        self.T = T
        self.lambda_ = lambda_t(0)  # argmax(lambda_t) = 0

    def experiment(self):
        T = self.T
        lambda_t = self.lambda_t
        lambda_ = self.lambda_
        return cd.non_homogeneous_poisson_process(T, lambda_t, lambda_)

    def run(self):
        events = self.experiment()
        tools.print_stats(events)


if __name__ == '__main__':
    One().run(True)
    Two().run(True)
    Four().run(True)
    SevenA().run(True)
    SevenB().run(True)
    Eleven().run()
    Twelve().run()
