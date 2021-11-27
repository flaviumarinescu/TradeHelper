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


def extract(**kwargs) -> Tuple[pd.DataFrame, str]:
    df = yf.download(**kwargs)
    if isinstance(df, pd.DataFrame):
        if not df.empty:
            return df, kwargs["tickers"]
    raise RuntimeError("Data in invalid")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = map(str.lower, df.columns)
    df.index.name = df.index.name.lower()
    df.index = pd.to_datetime(df.index)

    df = common_clean(df)

    if not df.empty:
        i = df.index[-1].time()  # since data is from yahoo finance... we need to adapt
        if not (i.second == 0 and (i.minute == 30 or i.minute == 0)):
            return df[:-1]
        else:
            return df
    else:
        raise RuntimeError("Data in invalid")
