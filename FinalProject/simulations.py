from random import random
from random import seed
from math import log


def exponential(lambda_):
    """Exponential distribution."""
    U = random()
    return (-log(U)) / lambda_


def simulation(n, spare, Tf, Tg):
    assert n > 0
    assert spare >= 0

    def random_fail(): return exponential(1 / Tf)

    def random_fix(): return exponential(1 / Tg)

    inf = float('inf')
    fails = [random_fail() for i in range(n)]
    fails.sort()
    t = 0
    broken = 0
    t_fixed = inf

    while True:
        if fails[0] < t_fixed:
            t = fails[0]
            broken += 1
            if broken >= spare + 1:
                return t
            if broken < spare + 1:
                fails[0] = t + random_fail()
                fails.sort()
                spare -= 1
            if broken == 1:
                t_fixed = t + random_fix()
        else:
            t = t_fixed
            broken -= 1
            if broken > 0:
                t_fixed = t + random_fix()
            if broken == 0:
                t_fixed = inf


if __name__ == '__main__':
    n = 5
    spare = 2
    Tf = 1
    Tg = 0.125

    while True:
        t = simulation(n, spare, Tf, Tg)
        print(t)
