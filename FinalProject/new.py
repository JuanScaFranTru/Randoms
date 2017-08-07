def simulation(n, spare, Tf, Tg, oper):
    inf = float('inf')
    fails = [random_fail() for i in range(n)]
    fails.sort()
    t = 0
    broken = 0
    fixing = 0
    # 'oper' operarios
    t_fixed = [inf] * oper

    while True:

        if fails[0] < t_fixed[oper - 1]:
            t = fails[0]
            broken += 1

            if broken >= spare + 1:
                return t

            if broken < spare + 1:
                fails[0] = t + random_fail()
                fails.sort()

            i = 0
            while broken > fixing and t_fixed[i] == inf:
                t_fixed[i] = t + random_fix()
                fixing += 1
                i += 1
            t_fixed.sort(reverse=True)

        else:
            t = t_fixed[oper - 1]
            broken -= 1
            fixing -= 1

            if broken == fixing:
                t_fixed[oper - 1] = inf

            if broken > fixing:
                t_fixed[oper - 1] = t + random_fix()
                fixing += 1
            t_fixed.sort(reverse=True)
