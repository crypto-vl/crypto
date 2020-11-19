load("lib.py")

import random

def bperm(t1,t2,t3,t4):
    t1 = ensure_vec(t1)
    t2 = ensure_vec(t2)
    t3 = ensure_vec(t3)
    t4 = ensure_vec(t4)

    r1 = B([0,0,0,0])
    r2 = B([0,0,0,0])
    r3 = B([0,0,0,0])
    r4 = B([0,0,0,0])

    r1[0] = t1[0]
    r1[1] = t2[0]
    r1[2] = t3[0]
    r1[3] = t4[0]

    r2[0] = t1[1]
    r2[1] = t2[1]
    r2[2] = t3[1]
    r2[3] = t4[1]

    r3[0] = t1[2]
    r3[1] = t2[2]
    r3[2] = t3[2]
    r3[3] = t4[2]

    r4[0] = t1[3]
    r4[1] = t2[3]
    r4[2] = t3[3]
    r4[3] = t4[3]

    return r1, r2, r3, r4

def bround(m1,m2,m3,m4,k1,k2,k3,k4):
    t1 = S(k1+m1)
    t2 = S(k2+m2)
    t3 = S(k3+m3)
    t4 = S(k4+m4)
    return t1,t2,t3,t4

def blastkey(m1,m2,m3,m4, k1,k2,k3,k4):
    return m1+k1,m2+k2,m3+k3,m4+k4



def cround(m,k):
    m1, m2, m3, m4 = string2b(m)
    k1, k2, k3, k4 = string2b(k)
    t1,t2,t3,t4 = bround(m1,m2,m3,m4,k1,k2,k3,k4)
    return b2string(t1,t2,t3,t4)


def perm(x):
    t1, t2, t3, t4 = string2b(x)
    r1, r2, r3, r4 = bperm(t1, t2, t3, t4)
    return b2string(r1, r2, r3, r4)


def lastkey(m, k):
    return addb(m,k)



def full_round(m, key_list):
    m_list = string2b(m)
    for i in range(4):
        k_list = string2b(key_list[i])
        m_list = bround(m_list[0],m_list[1],m_list[2],m_list[3], k_list[0],k_list[1],k_list[2],k_list[3])
        m_list = bperm(m_list[0],m_list[1],m_list[2],m_list[3])

    k_list = string2b(key_list[4])
    m_list = bround(m_list[0],m_list[1],m_list[2],m_list[3], k_list[0],k_list[1],k_list[2],k_list[3])

    k_list = string2b(key_list[5])

    return b2string(m_list[0] + k_list[0],m_list[1] + k_list[1],m_list[2] + k_list[2],m_list[3] + k_list[3] )

def partial_round(m, key_list):
    m_list = string2b(m)
    for i in range(len(key_list)):
        k_list = string2b(key_list[i])
        m_list = bround(m_list[0],m_list[1],m_list[2],m_list[3], k_list[0],k_list[1],k_list[2],k_list[3])
        m_list = bperm(m_list[0],m_list[1],m_list[2],m_list[3])

    return b2string(m_list[0],m_list[1],m_list[2],m_list[3])


def compute_full_diff(m, delta, key_list):
    c1 = full_round(m, key_list)
    c2 = full_round(addb(m,delta), key_list)
    return addb(c1,c2)


def compute_partial_diff(m, delta, key_list):
    c1 = partial_round(m, key_list)
    c2 = partial_round(addb(m,delta), key_list)
    return addb(c1,c2)


hx = '0123456789abcdef'
allin = [a+b+c+d for a in hx for b in hx for c in hx for d in hx]

k1='5b92'
k2='064b'
k3='1e03'
k4='a55f'
k5='ecbd'
k6='7ca5'

key_lst = [k1,k2,k3,k4,k5,k6]

delta = '0020'
test = ['0010', '0020', '0090', '00a0']

def check_good(c1,c2):
    if addb(c1,c2) in test:
        return True
    else:
        return False

def attackCh4(N):
    '''
    usees the four round differential 0020 --R4-->0020
    '''
    d = n2b(0x2)
    stat = [0 for i in range(16)]

    for dummy in range(N):
        m = random.choice(allin)
        c1 = full_round(m,key_lst)
        c2 = full_round(addb(m,delta),key_lst)
        if check_good(c1,c2):
            p1 = n2b(int(c1[2],16))
            p2 = n2b(int(c2[2],16))
            for k in B:
                if Sinv(p1+k) + Sinv(p2+k) == d:
                    stat[ b2n(k) ]+=1
    return stat, hex(stat.index(max(stat)))


def how_many_good_pairs(klst):
    cntr = 0
    for i in allin:
        j = addb(i, '0020')
        c1 = full_round(i, klst)
        c2 = full_round(j, klst)
        if check_good(c1, c2):
            cntr += 1
    return cntr
