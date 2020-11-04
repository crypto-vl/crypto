load("lib.sage")

def enc3(m, k1, k2, k3, k4):
    x = S(S(m+k1)+k2)
    y = x + k3
    z = S(y)
    c = z + k4
    return x, y, z, c


def S2_stat(n):
    for ib in B:
        f = n2b(n)
        jb = ib+f
        for k2 in B:
            print('i={}, j={}, S(S(i)+k2)+S(S(j)+k2)={}'.format( b2nh(ib), b2nh(jb), b2nh(S(S(ib)+k2) + S(S(jb)+k2)) ))


def attack3(N, k1, k2, k3, k4, delta, diff):
    '''
    Here delta = 0xf and diff = 0xc
    
    Do N attempts.
    Choose a block m, encrypt m and m + delta to c1 and c2.
    For every guessed key k4, compute y1 and y2.
    If y1 + y2 == diff, k4 is a candidate for the correct
    key, because diff is to occur with prob 15/64 as
    output difference: 0xf -> S -> 0xd is 10/16,
    0xd -> S -> 0xc is 6/16.
    '''

    stat = [0 for i in range(16)]

    for r in range(N):
        m = B.random_element()
        _,y1,_,c1 = enc3(m, k1, k2, k3, k4)
        _,y2,_,c2 = enc3(m+delta, k1, k2, k3, k4)

        for ki in range(16):
            k = n2b(ki)
            y1 = Sinv(k+c1)
            y2 = Sinv(k+c2)
            if y1+y2 == diff:
                stat[ki]+=1
    return stat, n2b(stat.index(max(stat)))


def attack3A(k1, k2, k3, k4, delta, diff):
    '''
    Here delta = 0xf and diff = 0xc

    Guess a key k4 = ki.
    For all blocks m, encrypt m and m + delta to c1 and c2.
    For every guessed key k4, compute y1 and y2.
    If y1 + y2 == diff, k4 is a candidate for the correct
    key, because diff is to occur with prob 15/64 as
    output difference: 0xf -> S -> 0xd is 10/16,
    0xd -> S -> 0xc is 6/16.
    '''

    stat = [0 for i in range(16)]
    
    for ki in range(16):
        k = n2b(ki)
        for m in B:
            _,y1,_,c1 = enc3(m, k1, k2, k3, k4)
            _,y2,_,c2 = enc3(m+delta, k1, k2, k3, k4)
            y1 = Sinv(k+c1)
            y2 = Sinv(k+c2)
            if y1+y2 == diff:
                stat[ki]+=1
    return stat, n2b(stat.index(max(stat)))

def problem(m,k):
    return(S(S(m)+k) + S(S(m+B([1,1,1,1]))+k))

def two_round():
    '''
    We consider m->S(m)->S(m)+k->S(S(m)+k)
    '''
    cnt = matrix(16)
    for k in B:
        nk= b2n(k)
        for m in B:
            x = problem(m,k)
            nx = b2n(x)
            cnt[nk,nx]+=1
    return cnt
        