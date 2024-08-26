import re
import pandas as pd
from numpy import nan


def nan_value(column_format: str):
    """
    Returns the NaN value for a given column format.

    Parameters:
    column_format (str): The format of the column.

    Returns:
    int or float or None: The NaN value corresponding to the column format.
                          Returns None if the column format is not recognized.
    """
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


def read_OMNI(filepath: str, formatpath: str):
    """
    Read OMNI data from a CSV file and apply formatting based on a format file.

    Args:
        filepath (str): The path to the CSV file containing the OMNI data.
        formatpath (str): The path to the format file containing the column formatting information.

    Returns:
        pandas.DataFrame: A DataFrame containing the formatted OMNI data.

    """
    df = pd.read_csv(
        filepath_or_buffer=filepath,
        parse_dates=[[0, 1, 2, 3]],
        date_format="%Y %j %H %M",
        sep=r"\s+",
        header=None,
    )

    with open(formatpath, "r") as f:
        format_file = f.read().split("\n")[8:-1]  # ignoring date/time and file header
        columns = ["Datetime"]
        types = [None]
        for _, row in enumerate(format_file):
            format_row = re.split(r",*\s+", row.strip())
            column_name = [format_row[1]]
            if column_name[0] in columns:
                column_name.append(format_row[-2])
            columns.append(", ".join(column_name))
            types.append(format_row[-1])

    df.columns = columns
    for i, encoding in enumerate(types):
        try:
            df.loc[df[columns[i]] == nan_value(encoding), columns[i]] = nan
        except KeyError:
            pass
    return df
