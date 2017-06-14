from continuous.distributions import normal

from math import sqrt, exp
from random import random, uniform
import scipy.stats as st


def zeta(alpha):
    return st.norm.ppf(1 - alpha)


class Exercise(object):
    def __init__(self):
        name = self.__class__.__name__
        msg = 'Exercise {}'.format(name)
        print()
        print(msg)
        print(len(msg) * '-')


class Simulator(Exercise):
    def __init__(self, niter, min_std_dev):
        super().__init__()
        self.niter = niter
        self.min_std_dev = min_std_dev

    def simulate(self):
        x = self.generator()
        y = self.generator()
        mean = (x + y) / 2
        var = (x - mean) ** 2 + (y - mean) ** 2

        j = 2
        while j < self.niter or sqrt(var / j) > self.min_std_dev:
            j += 1
            x = self.generator()
            old_mean = mean
            mean = mean + 1 / j * (x - mean)
            var = (1 - 1/(j - 1)) * var + j * (mean - old_mean) ** 2

        return mean, var, j

    def run(self):
        mean, var, n = self.simulate()
        print("n: {} >= {}".format(n, self.niter))
        print("Mean: {:2.3f}".format(mean))
        print("Var: {:2.3f}".format(var))
        print("sqrt(var / n): {} < {}".format(sqrt(var / n), self.min_std_dev))
        return mean, var, n


class SimulatorWithInterval(Simulator):
    def __init__(self, niter, min_std_dev, confidence):
        super().__init__(niter, min_std_dev)
        self.alpha = 1 - confidence

    def run(self):
        mean, var, n = super().run()
        delta = zeta(self.alpha / 2) * sqrt(var / n)
        interval_length = 2 * delta

        print('Interval: ({:2.3f}, {:2.3f})'.format(mean - delta,
                                                    mean + delta))
        print('Interval length: {:2.3f}'.format(interval_length))
        print('Delta: {:2.3f}'.format(delta))
        return mean, var, n


class One(Simulator):
    def __init__(self, niter=30, min_std_dev=0.1):
        super().__init__(niter, min_std_dev)

    def generator(self):
        return normal(0, 1)


class Two(Simulator):
    def __init__(self, niter=100, min_std_dev=0.01):
        super().__init__(niter, min_std_dev)

    def generator(self):
        return exp(random() ** 2)


class Three(SimulatorWithInterval):
    def __init__(self, niter=1000, confidence=0.95):
        super().__init__(niter, float('inf'), confidence)

    def generator(self):
        n = 0
        s = 0
        while s < 1:
            n += 1
            s += random()
        return n


class Four(SimulatorWithInterval):
    def __init__(self, niter=1000, confidence=0.95):
        super().__init__(niter, float('inf'), confidence)

    def generator(self):
        n = 1
        U = random()
        while True:
            n += 1
            V = random()
            if U > V:
                break
            U = V
        return n


class Five(SimulatorWithInterval):
    def __init__(self, niter=100, alpha=0.95, L=0.1):
        min_std_dev = L / (2 * zeta(alpha / 2))
        super().__init__(niter, min_std_dev, alpha)

    def generator(self):
        X = uniform(-1, 1)
        Y = uniform(-1, 1)
        if sqrt(X ** 2 + Y ** 2) <= 1:
            return 1
        return 0

    def simulate(self):
        x = self.generator()
        y = self.generator()
        p = (x + y) / 2

        j = 2
        while j < self.niter or sqrt((1 - p) * p / j) > self.min_std_dev:
            j += 1
            x = self.generator()
            p = p + 1 / j * (x - p)

        return 4 * p, 16 * (1 - p) * p, j


if __name__ == '__main__':
    One().run()
    Two().run()
    Three().run()
    Four().run()
    Five().run()
