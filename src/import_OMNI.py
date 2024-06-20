import pandas as pd
import re
from numpy import nan


def nan_value(column_format: str):
    match column_format:
        case "I3":
            return 99
        case "I4":
            return 999
        case "I7":
            return 999999
        case "F6.2":
            return 99.99
        case "F8.2":
            return 9999.99
        case "F8.1":
            return 99999.9
        case "F7.2":
            return 999.99
        case "F9.0":
            return 9999999
        case "F6.1":
            return 999.9
        case "I6":
            return 99999
        case "F7.3":
            return 9.999
        case "F5.1":
            return 99.9
        case "F9.2":
            return 99999.99
        case _:
            return None


def read_OMNI(filepath: str, formatpath: str, return_columns=False):
    df = pd.read_csv(
        filepath_or_buffer=filepath,
        parse_dates=[[0, 1, 2, 3]],
        date_format="%Y %j %H %M",
        delim_whitespace=True,
        header=None,
    )

    with open(formatpath, "r") as f:
        format_file = f.read().split("\n")[8:-1]  # ignoring date/time and file header
        columns = ["Datetime"]
        types = [None]
        for i, row in enumerate(format_file):
            format_row = re.split(r",*\s+", row.strip())
            columns.append(format_row[1])
            types.append(format_row[-1])

    df.columns = columns
    for i, format in enumerate(types):
        df.loc[df[columns[i]] == nan_value(format), columns[i]] = nan

    if return_columns:
        return df, columns
    return df
