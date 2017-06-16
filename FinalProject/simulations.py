from random import random
from math import log


def exponential(lambda_):
    """Exponential distribution."""
    U = random()
    return (-log(U)) / lambda_


class Simulation(object):
    def __init__(self):
        name = self.__class__.__name__
        msg = 'Simulation {}'.format(name)
        print()
        print(msg)
        print(len(msg) * '-')

    def run(self, N, S, Tf, Tr):
        pass


class One(Simulation):
    """Inicializar el programa con un sorteo de los tiempos de fallos de cada
    una las máquinas en uso, y ejecutarlo para estimar el tiempo medio de falla
    del sistema y su correspondiente desviación estándar.

    Expresar todos los tiempos usando como unidad el mes. Utilizar:
    N = 5, S = 2, y suponer que el tiempo medio de fallo de una máquina es
    Tf = 1 mes y que el tiempo medio medio de reparación de una máquina es
    Tr = 1/8 mes.

    Se realizan 10000 simulaciones de tiempos de fallo.
    """
    def __init__(self, N, S, Tf, Tr, nsim=1):
        """
        :param N: Number of in service machines
        :param S: Number of spare machines
        :param Tf: Mean time until a machine fails
        :param Tr: Repairing mean time (one machine)
        :param nsim: Number of simulations
        """
        for _ in range(nsim):
            mean_t, dev_t = self.run(N, S, Tf, Tr)
        self.mean_t = mean_t
        self.dev_t = dev_t



if __name__ == '__main__':
    pass
