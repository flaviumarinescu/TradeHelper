"""
    Pipeline functionality for yahoo finance.
"""

from datetime import datetime, timedelta
from typing import Tuple
import pandas as pd
import yfinance as yf
from . import common_clean


YF_PARAMS = {
    "tickers": "eurusd=x",
    "start": datetime.now() - timedelta(days=120),
    "end": datetime.now(),
    "interval": "60m",
    "rounding": False,
    "prepost": False,
    "progress": False,
    "group_by": "ticker",
}


def extract(**kwargs: YF_PARAMS) -> Tuple[pd.DataFrame, str]:
    """Extracts data from yahoo finance.

    Raises:
        RuntimeError: In case return data is not as expected.

    Returns:
        Tuple[pd.DataFrame, str]: Raw dataframe and ticker symbol.
    """
    dataframe = yf.download(**kwargs)
    if isinstance(dataframe, pd.DataFrame):
        if not dataframe.empty:
            return dataframe, kwargs["tickers"]
    raise RuntimeError("Data in invalid")


def clean(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Cleans extracted data from yahoo finance.

    Args:
        dataframe (pd.DataFrame): Raw dataframe form the above, extract, function.

    Raises:
        RuntimeError: In case cleaning resulted in an empty dataframe.

    Returns:
        pd.DataFrame: Processed, ready to use, dataframe
            * Check for final intended format in __init__.py, common_clean()
    """
    dataframe.columns = map(str.lower, dataframe.columns)
    dataframe.index.name = dataframe.index.name.lower()
    dataframe.index = pd.to_datetime(dataframe.index)

    dataframe = common_clean(dataframe)

    if not dataframe.empty:
        i = dataframe.index[
            -1
        ].time()  # since data is from yahoo finance... we need to adapt
        if not (i.second == 0 and (i.minute in (30, 0))):
            return dataframe[:-1]
        return dataframe
    raise RuntimeError("Data in invalid")
