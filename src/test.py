import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from import_OMNI import read_OMNI
from entropy import H, MI, CMI, entropy_matrix

if __name__ == "__main__":
    df = read_OMNI(
        filepath="datasets/test_AE_SYM_ASY_all.txt",
        formatpath="data_format/test_AE_SYM_ASY_all_format.txt",
    )
    # for column in list(df)[1:]:
    #     plt.plot(df["Datetime"], df[column], label=column)
    # plt.plot(df["Datetime"], df["BZ"], label="BZ")
    # plt.plot(df["Datetime"], df["SYM/H"], label="SYM/H")
    # plt.hist(df["SYM/H"], 150)
    # plt.legend()
    # plt.show()
    # entropy_matrix(df)
    print(H(df["BZ"].to_numpy(), bins= 200))
    print(MI(df["BZ"].to_numpy(), df["SYM/H"].to_numpy(), bins= 200))
    print(entropy_matrix(df))

