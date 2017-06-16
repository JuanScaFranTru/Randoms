from random import random
from math import log, sqrt
from numpy import mean, var


def exponential(lambda_):
    """Exponential distribution."""
    U = random()
    return (-log(U)) / lambda_


def simulation1(n, spare, Tf, Tg):
    """
    Inicializar el programa con un sorteo de los tiempos de fallos de cada una
    las máquinas en uso, y ejecutarlo para estimar el tiempo medio de falla del
    sistema y su correspondiente desviación estándar.

    Expresar todos los tiempos usando como unidad el mes.
    Utilizar: N = 5, S = 2, y suponer que el tiempo medio de fallo de una
    máquina es T F = 1 mes y que el tiempo medio medio de reparación de una
    máquina es T R = 1/8 mes.
    """
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
            if broken == 1:
                t_fixed = t + random_fix()
        else:
            t = t_fixed
            broken -= 1
            if broken > 0:
                t_fixed = t + random_fix()
            if broken == 0:
                t_fixed = inf


def simulation2(n, spare, Tf, Tg, oper):
    """Ahora hay 2 reparadores."""
    assert n > 0
    assert spare >= 0

    def random_fail(): return exponential(1 / Tf)

    def random_fix(): return exponential(1 / Tg)

    inf = float('inf')
    fails = [random_fail() for i in range(n)]
    fails.sort()
    t = 0
    broken = 0
    # Dos operarios
    t_fixed = [inf] * oper

    while True:
        # Se rompe una antes de que alguno de los dos operarios termine de
        # arreglar
        if fails[0] < t_fixed[oper - 1]:
            print(broken, t, t_fixed, fails)
            t = fails[0]
            broken += 1
            if broken >= spare + 1:
                return t
            if broken < spare + 1:
                fails[0] = t + random_fail()
                fails.sort()
            i = 0
            while i < oper and t_fixed[i] == inf and i < broken:
                t_fixed[i] = t + random_fix()
                i += 1
            t_fixed.sort(reverse=True)
        else:
            t = t_fixed[oper - 1]
            broken -= 1
            if broken > 0:
                t_fixed[oper - 1] = t + random_fix()
            if broken == 0:
                t_fixed[oper - 1] = inf
            t_fixed.sort(reverse=True)


if __name__ == '__main__':
    N = 5
    S = 2
    Tf = 1
    Tg = 0.125
    niter = 2
    oper = 2
    two_Ts = [0] * niter
    Ts = [0] * niter
    for i in range(niter - 1):
        t = simulation1(N, S, Tf, Tg)
        Ts[i] = t

        t2 = simulation2(N, S, Tf, Tg, oper)
        two_Ts[i] = t2

    mean1 = mean(Ts)
    dev1 = sqrt(var(Ts))

    mean2 = mean(two_Ts)
    dev2 = sqrt(var(two_Ts))

    print("1 operario ")
    print("Mean =", mean1)
    print("Dev =", dev1)

    print("\n2 operarios")
    print("Mean =", mean2)
    print("Dev =", dev2)
