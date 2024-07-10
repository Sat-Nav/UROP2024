from spacepy import pycdf
import pandas as pd

def read_CDAWeb(mag_file_path, swepam_file_path):
    mag = pycdf.CDF(mag_file_path)
    swepam = pycdf.CDF(swepam_file_path)

    d = {"Epoch" : mag["Epoch"][...]}
    for i, coord in enumerate(mag["metavar0"][...]):
        d[coord] = mag["BGSM"][...][:,i]
    mag_df = pd.DataFrame.from_dict(d)

    d = {}
    for i in swepam:
        d[i] = swepam[i][...]
    swepam_df = pd.DataFrame.from_dict(d)
    return mag_df, swepam_df