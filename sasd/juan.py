from random import uniform, random
from math import sqrt, log, exp


class ej1:
    def twonormal2(mu, sigma):
        """Return two normal distributed random variables."""
        while True:
            U1, U2 = uniform(-1, 1), uniform(-1, 1)
            S = U1 ** 2 + U2 ** 2
            if S <= 1:
                break

        tmp = sqrt(-2 * log(S) / S)
        return U1 * tmp, U2 * tmp

    def mean_estimation(min_simlation, accept_value):
        mean = 0
        var = 0
        data_len = 0
        while data_len < min_simlation or (var / data_len) ** (1/2) > accept_value:
            data_len += 1
            X, _ = ej1.twonormal2(0, 1)
            old_mean = mean
            mean += 1 / data_len * (X - mean)
            if var != 0:
                var *= (1 - 1 / (data_len - 1))
            var += data_len * (mean - old_mean)**2
        return (mean, var, data_len)

    def simulation():
        n = 30
        acceptable_value = 0.1

        mean, var, data_len = ej1.mean_estimation(n, acceptable_value)

        print("Mean = ", mean, "\nVariance = ", var, "\nStd Desv = ", var ** (1/2),
              "\nGenerated Values = ", data_len)


class ej2:
    def mean_estimation(min_simlation, accept_value=float('-inf')):
        mean = 0
        var = 0
        data_len = 0
        while data_len < min_simlation or sqrt(var / data_len) > accept_value:
            data_len += 1
            X = exp(random() ** 2)
            old_mean = mean
            mean += (X - mean) / data_len
            if var != 0:
                var *= 1 - 1 / (data_len - 1)
            var += data_len * (mean - old_mean) ** 2
            # Or (is much better the aproximation, tradeoff with time)
            # var += float(data_len * (mean - old_mean)) ** 2

        return (mean, var, data_len)

    def simulation():
        n = 100
        acceptable_value = 0.01  # Std Desviation ** 2 == var

        mean, var, data_len = ej2.mean_estimation(n, acceptable_value)

        print("Mean = ", mean, "\nVariance = ", var, "\nStd Desv = ", var ** (1/2),
              "\nGenerated Values = ", data_len)


class ej3:
    def N():
        sum_U = uniform(0, 1)
        niter = 0
        while sum_U <= 1:
            niter += 1
            sum_U += uniform(0, 1)
        return niter

    def mean_estimation(nsimulation):
        mean = 0
        var = 0
        for data_len in range(1, nsimulation + 1):
            X = ej3.N()
            old_mean = mean
            mean += (X - mean) / data_len
            if var != 0:
                var *= 1 - 1 / (data_len - 1)
            var += data_len * (mean - old_mean) ** 2
            # Or (is much better the aproximation, tradeoff with time)
            # var += float(data_len * (mean - old_mean)) ** 2
        return (mean, var, data_len)

    def simulation():
        n = 1000

        mean, var, data_len = ej3.mean_estimation(n)
        interval = (mean - 1.96 * sqrt(var / n), mean + 1.96 * sqrt(var / n))

        print("Mean = ", mean, "\nVariance = ", var, "\nStd Desv = ", var ** (1/2),
              "\nGenerated Values = ", data_len)
        print("Intervalo:", interval)


class ej4:
    def M():
        i = 1
        U, new_U = random(), random()
        while U <= new_U:
            U, new_U = new_U, random()
            i += 1
        return i

    def mean_estimation(nsimulation):
        mean = 0
        var = 0
        data_len = 0
        for i in range(nsimulation):
            # Or (is much better the aproximation, tradeoff with time)
            # while data_len < min_simlation or
            # sqrt(var / data_len) > accept_value:
            data_len += 1
            X = ej4.M()
            old_mean = mean
            mean += (X - mean) / data_len
            if var != 0:
                var *= 1 - 1 / (data_len - 1)
            var += data_len * (mean - old_mean) ** 2
            # Or (is much better the aproximation, tradeoff with time)
            # var += float(data_len * (mean - old_mean)) ** 2

        return (mean, var, data_len)

    def simulation():
        n = 10000

        mean, var, data_len = ej4.mean_estimation(n)
        # interval = (mean - 1.96 * sqrt(var / n), mean + 1.96 * sqrt(var / n))

        print("Mean = ", mean, "\nVariance = ", var, "\nStd Desv = ", var ** (1/2), type(var ** (1/2)),
              "\nGenerated Values = ", data_len)
