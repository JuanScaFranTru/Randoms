

class Simulation(object):
    def __init__(self):
        name = self.__class__.__name__
        msg = 'Exercise {}'.format(name)
        print()
        print(msg)
        print(len(msg) * '-')

    def run(self, N, S, Tf, Tr):
        pass


class One(Simulation):

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
