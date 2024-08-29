import os
import pandas as pd


def read_RTSW_ACE(base_path, year, *args):
    """
    Read RTSW ACE data files for a specified date.

    Parameters:
    - base_path (str): The base path where the data files are located.
    - year (int): The year of the data files.
    - *args (int): Variable length argument list representing the month and day.

    Returns:
    - mag_df (pd.DataFrame): Dataframe containing Magnetometer data.
    - swepam_df (pd.DataFrame): Dataframe containing Solar Wind Electron Proton Alpha Monitor data.

    Raises:
    - ValueError: If the year is not specified or is not a four-digit number.
    - ValueError: If the month or day is not a one or two-digit number.
    - FileNotFoundError: If no Magnetometer data is found for the specified date.
    - FileNotFoundError: If no Solar Wind Electron Proton Alpha Monitor data is found for the specified date.
    """

    if not year:
        raise ValueError("Year must be specified.")
    try:
        year = str(year)
        if len(year) != 4:
            raise ValueError("Year must be a four-digit number.")
    except ValueError as exc:
        raise ValueError("Year must be a four-digit number.") from exc

    date_selection = [year]
    if len(args) > 2:
        raise ValueError("Only month and day can be specified")
    for _, entry in enumerate(args):
        try:
            entry = str(entry)
            date_selection.append(entry.zfill(2))
            if len(entry) > 2:
                raise ValueError("Month and day must be one or two-digit numbers.")
        except ValueError as exc:
            raise ValueError("Month and day must be one or two-digit numbers.") from exc

    base_path += f"/{year}"
    file_prefix = ""
    for entry in date_selection:
        file_prefix += entry

    mag_path = "/".join([base_path, "mag"])
    swepam_path = "/".join([base_path, "swepam"])

    # Read files from the specified path
    mag_files = [file for file in os.listdir(mag_path) if (file.startswith(file_prefix) and not file.endswith("5m.dat"))]
    swepam_files = [file for file in os.listdir(swepam_path) if (file.startswith(file_prefix) and not file.endswith("5m.dat"))]

    if len(mag_files) == 0:
        raise FileNotFoundError("No Magnetometer data found for the specified date.")
    if len(swepam_files) == 0:
        raise FileNotFoundError("No Solar Wind Electron Proton Alpha Monitor data found for the specified date.")

    mag_df = pd.concat(
        [pd.read_csv(
            filepath_or_buffer="/".join([mag_path, file]),
            sep=r"\s+",
            header=None,
            usecols=[0, 1, 2, 3, 6, 7, 8, 9, 10],
            skiprows=20,
            na_values=-999.9,
            dtype = {0: str, 1: str, 2: str, 3: str},
            names = ["Year", "Month", "Day", "HM", "State", "Bx", "By", "Bz", "Bt"]
        )
            for file in mag_files]
    )
    mag_df.insert(
        loc=0,
        column="Datetime",
        value=pd.to_datetime(mag_df[["Year", "Month", "Day", "HM"]].apply(lambda x: '-'.join(x), axis=1), format = "%Y-%m-%d-%H%M"))
    
    mag_df = mag_df.drop(["Year", "Month", "Day", "HM"], axis=1)
    swepam_df = pd.concat(
        [pd.read_csv(
            filepath_or_buffer="/".join([swepam_path, file]),
            sep=r"\s+",
            header=None,
            usecols=[0, 1, 2, 3, 6, 7, 8, 9],
            skiprows=18,
            na_values={7:-9999.9, 8:-9999.9, 9:-1.00e+05},
            dtype = {0: str, 1: str, 2: str, 3: str},
            names = ["Year", "Month", "Day", "HM", "State", "Proton Density", "Velocity", "Temperature"]
        )
            for file in swepam_files]
    )
    swepam_df.insert(
        loc=0,
        column="Datetime",
        value=pd.to_datetime(swepam_df[["Year", "Month", "Day", "HM"]].apply(lambda x: '-'.join(x), axis=1), format = "%Y-%m-%d-%H%M"))
    
    swepam_df = swepam_df.drop(["Year", "Month", "Day", "HM"], axis=1)

    return mag_df.merge(swepam_df, on="Datetime")