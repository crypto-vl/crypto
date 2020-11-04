from lib import *
from chiffre1 import *


def run_candidate1(x, f):
    f(11, 7, x, b_add(x, 15))


def Ssquare(x, k):
    k_vec = ensure_vec(k)
    x_num = ensure_num(x)
    return S(S(x) + k_vec)


def two_char(k):
    res = [0 for x in range(16)]
    for m in B:
        c1 = Ssquare(m, k)
        c2 = Ssquare(m + n2b(0xf), k)
        res[b2n(c1 + c2)] += 1
    return res


if __name__ == '__main__':
    #    print(StatS())
    mean_v = [0 for x in range(16)]
    for k in range(16):
        stat = two_char(k)
        for i in range(16):
            mean_v[i] = mean_v[i] + stat[i]
        print(stat)
    print([x / 256 * 1.0 for x in mean_v])

    RR = matrix(16, 16)
    for dx in range(16):
        for a in range(16):
            dy = ensure_num(S(a) + S(b_add(a, dx)))
            print(dy)
            RR[dx, dy] += 1
    print(latex(RR))
