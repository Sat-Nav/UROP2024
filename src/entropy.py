import numpy as np
from scipy.stats import entropy
from sklearn.feature_selection import mutual_info_regression

def generate_hist(a, *args, bins=200):
    if args:
        series_diff = a.shape[0] - args[0].shape[0]
        if series_diff > 0:
            targ = np.pad(args[0], (0, series_diff), constant_values = np.nan)
        else:
            targ = args[0]
            a = np.pad(a, (0, -series_diff), constant_values = np.nan)
        nans = np.logical_or(np.isnan(a), np.isnan(targ))
        for arg in args[1:]:
            series_diff = nans.shape[0] - arg.shape[0]
            if series_diff > 0:
                arg = np.pad(arg, (0, series_diff), constant_values = np.nan)
            else:
                a = np.pad(a, (0, -series_diff), constant_values = np.nan)
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

def shannon_entropy(p_i, use_scipy = False):
    if use_scipy:
        return entropy(p_i, base=2)
    return -sum(p_i*np.log2(p_i))

def H(x, y=None, *z, conditional=False, bins=200, use_scipy = False):
    if y is None:
        a = generate_hist(x, bins=bins)
        p_a = a/sum(a)
        return shannon_entropy(p_a, use_scipy=use_scipy)

    if conditional:
        return H(x, y, bins=bins, use_scipy=use_scipy) - H(y, bins=bins, use_scipy=use_scipy)

    ab = generate_hist(x, y, *z, bins=bins)
    p_ab = ab/sum(ab)
    return shannon_entropy(p_ab, use_scipy=use_scipy)

def MI(x, y, bins=200, use_scipy = False, use_sklearn = False):
    if use_sklearn:
        x, y = x.to_numpy(), y.to_numpy()
        if len(x.shape) == 1:
            x = x.reshape(-1,1)
        return mutual_info_regression(x, y, n_jobs= -6)
    return H(x, bins=bins, use_scipy=use_scipy) + H(y, bins=bins, use_scipy=use_scipy) - H(x,y, bins=bins, use_scipy=use_scipy)

def CMI(x, y, z, bins=200):
    return H(x, z, bins=bins) + H(y, z, bins=bins) - H(x, y, z, bins=bins) + H(z, bins=bins)

def entropy_matrix(df, bins=200, ignore_columns=[0], use_scipy = False, use_sklearn = False):
    columns = list(df)
    for i in ignore_columns:
        columns.pop(i)
    matrix = []
    for _, column_1 in enumerate(columns):
        if use_sklearn:
            row = MI(df[columns], df[column_1], bins=bins, use_sklearn=True)
        else:
            row = np.array([MI(df[column_1], df[column_2], bins=bins, use_scipy=use_scipy, use_sklearn=False) for column_2 in columns])
        matrix.append(row)
    return np.array(matrix)