from lib import *

def enc1(m, k0, k1):
    m = ensure_vec(m)
    k0 = ensure_vec(k0)
    k1 = ensure_vec(k1)
    u = m + k0
    v = S(u)
    e = v + k1
    return u, v, e


def candidate1(k0, k1, m1, m2):
    m1 = ensure_vec(m1)
    m2 = ensure_vec(m2)
    k0 = ensure_vec(k0)
    k1 = ensure_vec(k1)
    u1, v1, c1 = enc1(m1, k0, k1)
    u2, v2, c2 = enc1(m2, k0, k1)
    for k in B:
        v11 = c1 + k
        v22 = c2 + k
        u11 = Sinv(v11)
        u22 = Sinv(v22)
        if u11 + u22 == m1 + m2:
            print('candidate for k1: ' + b2nh(k))
