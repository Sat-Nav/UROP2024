from spacepy import pycdf
import pandas as pd

def read_CDAWeb(*files, mag_file_path=None):
    if mag_file_path:
        mag = pycdf.CDF(mag_file_path)

        d = {"Epoch" : mag["Epoch"][...]}
        for i, coord in enumerate(mag["metavar0"][...]):
            d[coord] = mag["BGSM"][...][:,i]
        mag_df = pd.DataFrame.from_dict(d)

    dfs = []
    for file in files:
        cdf = pycdf.CDF(file)
        d = {}
        for i in cdf:
            d[i] = cdf[i][...]
        dfs.append(pd.DataFrame.from_dict(d))
    return mag_df, *dfs