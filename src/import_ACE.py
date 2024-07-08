import pandas as pd
import datetime

def read_ACE(filepath: str):
    df = pd.read_csv(
        filepath_or_buffer=filepath,
        sep=r"\s+",
        header=0,
        skiprows=list(range(21))
    )
    origin_ts = int(datetime.datetime(1996, 1, 1, 0, 0, 0).timestamp())
    df[df.columns[0]] = df[df.columns[0]].apply(
        lambda x: datetime.datetime.fromtimestamp(origin_ts + x, datetime.UTC)
    ).dt.tz_convert(None)
    return df