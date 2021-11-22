import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from typing import Tuple
import redis
import pickle


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


def clean(df: pd.DataFrame, dropna: str = "any") -> pd.DataFrame:
    df.columns = map(str.lower, df.columns)
    date_column = df.columns[df.columns.str.contains("date")]
    if not date_column.empty:
        df.set_index(date_column.values[0], inplace=True)
    df.index = pd.to_datetime(df.index)

    if df.index.tz:
        df = df.tz_convert("Europe/Bucharest")
        df = df.tz_localize(None)

    if dropna:
        df.dropna(how=dropna, inplace=True)
    df = df.reindex(columns=["open", "high", "low", "close", "volume"])

    if not df.empty:
        i = df.index[-1].time()  # since data is from yahoo finance... we need to adapt
        if not (i.second == 0 and (i.minute == 30 or i.minute == 0)):
            return df[:-1]
        else:
            return df
    else:
        raise RuntimeError("Data in invalid")


def load(df: pd.DataFrame, ticker: str, cache: redis.Redis) -> bool:
    df_pickled = pickle.dumps(df, protocol=pickle.HIGHEST_PROTOCOL)
    return cache.set(ticker, df_pickled)
