from lib import *

def enc1(m, k0, k1):
    m_arg = ensure_vec(m)
    k0_arg = ensure_vec(k0)
    k1_arg = ensure_vec(k1)
    u = m_arg + k0_arg
    v = S(u)
    e = v + k1_arg
    return u, v, e


def candidate1(k0, k1, m1, m2):
    m1_arg = ensure_vec(m1)
    m2_arg = ensure_vec(m2)
    k0_arg = ensure_vec(k0)
    k1_arg = ensure_vec(k1)
    u1, v1, c1 = enc1(m1_arg, k0_arg, k1_arg)
    u2, v2, c2 = enc1(m2_arg, k0_arg, k1_arg)
    for k in B:
        v11 = c1 + k
        v22 = c2 + k
        u11 = Sinv(v11)
        u22 = Sinv(v22)
        if u11 + u22 == m1_arg + m2_arg:
            print('candidate for k1: ' + b2nh(k))
