
k = ensure_vec(0xa)

def func(delta):
    delta = ensure_vec(delta)
    for m in B:
        print( S(m+k) + S(m+delta+k) )
