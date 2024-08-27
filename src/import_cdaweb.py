from spacepy import pycdf
import pandas as pd

def read_CDAWeb(mag_path=None, swepam_path=None):
    if mag_path:
        mag = pycdf.CDF(mag_path)

        d = {"Epoch" : mag["Epoch"][...]}
        for i, coord in enumerate(mag["metavar0"][...]):
            d[coord] = mag["BGSM"][...][:,i]
        mag_df = pd.DataFrame.from_dict(d)

    if swepam_path:
        cdf = pycdf.CDF(swepam_path)
        d = {}
        for i in cdf:
            if i == "metavar0":
                continue
            if len(cdf[i][...].shape) == 1:
                values = cdf[i][...]
            else:
                for j, coord in enumerate(cdf["metavar0"][...]):
                    values = cdf[i][:,j]
            d[i] = values
        swepam_df = pd.DataFrame.from_dict(d)
    
    if mag_path and swepam_path:
        return mag_df, swepam_df
    elif mag_path:
        return mag_df
    elif swepam_path:
        return swepam_df
    return None