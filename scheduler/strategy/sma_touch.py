""""
    Functions to apply and validate strategy.
"""

import pandas as pd
from . import change_context


def apply(dataframe: pd.DataFrame, sma: int = 9, context: str = "4h") -> pd.DataFrame:
    """Add columns needed for strategy

    Args:
        dataframe (pd.DataFrame): Dataframe with open high low close columns and datetime index
        sma (int, optional): Moving average period. Defaults to 9.
        context (str, optional): Resample to specific timeframe. Defaults to "4h".

    Returns:
        pd.DataFrame: Returns processed dataframe.
    """
    dataframe = change_context(dataframe, to_timeframe=context)
    dataframe["sma"] = dataframe.close.rolling(sma).mean()
    dataframe.dropna(how="any", inplace=True)
    return dataframe


def is_valid(dataframe: pd.DataFrame) -> bool:
    """Check if last entry touches sma

    Args:
        dataframe (pd.DataFrame): Dataframe with open high low close columns and datetime index

    Returns:
        bool: True if last candle touches sma, False otherwise
    """
    entry = dataframe.iloc[-1]
    if entry.low <= entry.sma <= entry.high:
        return True
    return False
