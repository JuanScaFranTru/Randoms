from collections import Counter as Freq
from math import exp
from random import random
import svt.chi2 as c
import svt.kolmogorov as k


class Ej1:
    # 0 -> blancas
    # 1 -> rosas
    # 2 -> rojas
    def __init__(self):
        self.p = {0: 1 / 4, 1: 1 / 2, 2: 1/4}
        self.freq = list(Freq({0: 141, 1: 291, 2: 132}).elements())

    def chisqr(self):
        sample = self.freq
        print(c.chi2_test(sample, self.p))

    def simulation(self):
        sample = self.freq
        t, pvalue = c.chi2_test_simulate(sample, self.p, 1000)

        print(t, pvalue)


class Ej2:
    def __init__(self):
        self.p = {i: 1 / 6 for i in range(1, 7)}
        self.freq = list(Freq({1: 158, 2: 172, 3: 164,
                               4: 181, 5: 160, 6: 165}).elements())

    def chisqr(self):
        sample = self.freq
        print(c.chi2_test(sample, self.p))

    def simulation(self):
        sample = self.freq
        t, pvalue = c.chi2_test_simulate(sample, self.p, 1000)

        print(t, pvalue)


class Ej3:
    def simulation(self):
        def F(x):
            if x < 0:
                return 0
            elif x > 1:
                return 1
            else:
                return x
        sample = [0.12, 0.18, 0.06, 0.33, 0.72, 0.83, 0.36, 0.27, 0.77, 0.74]
        t, pvalue = k.kolmogorov_test(sample, F, 1000)

        print(t, pvalue)


class Ej4:
    def simulation(self):
        def F(x):
            return (1 - exp(- (1 / 50) * x))
        sample = [86, 133, 75, 22, 11, 144, 78, 122, 8, 146, 33, 41, 99]
        t, pvalue = k.kolmogorov_test(sample, F, 1000)

        print(t, pvalue)


if __name__ == '__main__':

    ej4 = Ej4()
    ej4.simulation()
