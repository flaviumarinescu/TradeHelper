"""
    Functionalities shared by multiple strategies.
"""

import pandas as pd


def change_context(dataframe: pd.DataFrame, to_timeframe: str) -> pd.DataFrame:
    """Changes granularity of dataframe

    Args:
        dataframe (pd.DataFrame): Dataframe with open high low close columns and datetime index
        to_timeframe (str): pd.resample compatible argument (4h, 1h, 1d ...)

    Returns:
        pd.DataFrame: Returns resampled dataframe.
    """
    dataframe = dataframe.resample(to_timeframe).agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    )
    dataframe.dropna(how="any", inplace=True)
    return dataframe
