import numpy as np

def generate_hist(a, b=None, bins=200):
    if b:
        n = np.histogram2d(a,b,bins=bins)[0]
        n = n[n!=0]
        return n
    a = a[~np.isnan(a)]
    n = np.histogram(a, bins=bins)[0]
    n = n[n!=0]
    return n

def shannon_entropy(p_i):
    return -sum(p_i*np.log2(p_i))

def H(x, y=None, bins=200):
    a = generate_hist(x, bins=bins)
    p_a = a/sum(a)
    Ha = shannon_entropy(p_a)
    if not y:
        return Ha
    
    # two implemenations for MI- thorough:
    b = generate_hist(y, bins=bins)
    p_b = b/sum(b)
    Hb = shannon_entropy(p_b)

    ab = generate_hist(x, y, bins=bins)
    p_ab = ab/sum(ab)
    Hab = shannon_entropy(p_ab)
    return Ha + Hb - Hab
    


