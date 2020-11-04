from lib import *


def enc2(m, k0, k1, k2):
    m = ensure_vec(m)
    k0 = ensure_vec(k0)
    k1 = ensure_vec(k1)
    k2 = ensure_vec(k2)
    u = m + k0
    v = S(u)
    w = v + k1
    x = S(w)
    c = x + k2
    return u, v, w, x, c


def sbox_stat(x):
    for y in B:
        print(b2nh(y), b2nh(x + y), b2nh(S(y) + S(x + y)))


def S_stat(n):
    for ib in B:
        f = n2b(n)
        jb = ib + f
        print('i={}, j={}, S(i)+S(j)={}'.format(b2nh(ib), hex(int(b2n(jb))), hex(int(b2n(S(ib) + S(jb))))))


def attack3(m, k1, k2, k3, delta, diff):
    '''
    For the message block m, encrypt m and m + delta to c1 and c2.
    For every key k3, compute w1 and w2.
    If w1 + w2 == diff, k3 is a candidate for the correct
    key, because diff is very likely to occur as
    output difference of S.
    '''
    stat = [0 for i in range(16)]

    _, v1, _, _, c1 = enc2(m, k1, k2, k3)
    _, v2, _, _, c2 = enc2(m + delta, k1, k2, k3)

    for k in B:
        w1 = Sinv(k + c1)
        w2 = Sinv(k + c2)
        if w1 + w2 == diff:
            stat[b2n(k)] += 1
    return stat, b2nh(n2b(stat.index(max(stat))))


def attack2(k1, k2, k3, delta, diff):
    '''
    For every message block m, encrypt m and m + delta to c1 and c2.
    For every key k3, compute w1 and w2.
    If w1 + w2 == diff, k3 is a candidate for the correct
    key, because diff is very likely to occur as
    output difference of S.
    '''
    stat = [0 for i in range(16)]

    res = matrix(16)
    allone = vector([1 for i in range(16)])

    for m in B:
        mn = b2n(m)
        _, v1, _, _, c1 = enc2(m, k1, k2, k3)
        _, v2, _, _, c2 = enc2(m + delta, k1, k2, k3)

        for k in B:
            w1 = Sinv(k + c1)
            w2 = Sinv(k + c2)
            if w1 + w2 == diff:
                res[mn, b2n(k)] += 1
    return res, allone * res

def attack_statistics(k0, k1, k2, delta, diff):
    k0 = ensure_vec(k0)
    k1 = ensure_vec(k1)
    k2 = ensure_vec(k2)
    delta = ensure_vec(delta)
    diff = ensure_vec(diff)
    
    stat = [0 for i in range(16)]
    for m in B:
        st, _ = attack3(m, k0, k1, k2, delta, diff)
        for i in range(16):
            stat[i] += st[i]
    print(stat)
    e = max(stat)
    for i in range(16):
        if stat[i] == e:
            print(n2b(i), i)
    
if __name__ == '__main__':
    k0 = n2b(0xb)
    k1 = n2b(0x3)
    k2 = n2b(0x9)
    delta = n2b(0xf)
    diff = n2b(0xd)
    attack_statistics(k0, k1, k2, delta, diff)