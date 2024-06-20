from import_OMNI import read_OMNI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df, columns = read_OMNI(
        filepath="datasets/test_AE_SYM_ASY_all.txt",
        formatpath="data_format/test_AE_SYM_ASY_all_format.txt",
        return_columns=True
    )
    print(columns)
    # for column in columns[1:]:
    #     plt.plot(df["Datetime"], df[column], label=column)
    # plt.plot(df["Datetime"], df["BZ"], label="BZ")
    # plt.plot(df["Datetime"], df["SYM/H"], label="SYM/H")
    # plt.hist(df["SYM/H"], 150)
    plt.hist(df["BZ"], 200)
    plt.legend()
    plt.show()
