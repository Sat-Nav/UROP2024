import numpy as np

def generate_hist(a, *args, bins=200):
    if args:
        nans = np.logical_or(np.isnan(a), np.isnan(args[0]))
        for arg in args[1:]:
            nans = np.logical_or(nans, np.isnan(arg))
        variables = []
        for _, arg in enumerate(args):
            variables.append(arg[~nans])
        a = a[~nans]
        n = np.histogramdd(np.array([a,*variables]).T, bins=bins)[0]
        n = n[n!=0]
        return n
    
    a = a[~np.isnan(a)]
    n = np.histogram(a, bins=bins)[0]
    n = n[n!=0]
    return n

def shannon_entropy(p_i):
    return -sum(p_i*np.log2(p_i))

def H(x, y=None, *z, conditional=False, bins=200):
    if y is None:
        a = generate_hist(x, bins=bins)
        p_a = a/sum(a)
        return shannon_entropy(p_a)

    if conditional:
        return H(x, y, bins=bins) - H(y, bins=bins)

    ab = generate_hist(x, y, *z, bins=bins)
    p_ab = ab/sum(ab)
    return shannon_entropy(p_ab)


def MI(x, y, bins=200):
    return H(x, bins=bins) + H(y, bins=bins) - H(x,y, bins=bins)

def CMI(x, y, z, bins=200):
    return H(x, z, bins=bins) + H(y, z, bins=bins) - H(x, y, z) - H(z)

def entropy_matrix(df, bins=200):
    columns = list(df)
    matrix = []
    for _, column_1 in enumerate(columns):
        if column_1 == "Datetime":
            continue
        row = []
        for __, column_2 in enumerate(columns):
            if column_2 == "Datetime":
                continue
            row.append(MI(df[column_1], df[column_2], bins=bins))
        matrix.append(row)
    return np.array(matrix)