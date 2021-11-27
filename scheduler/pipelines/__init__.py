from typing import Any
import pandas as pd
import redis
import pickle


def load(obj: Any, key: str, cache: redis.Redis) -> bool:
    pickeld_ob = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    return cache.set(key, pickeld_ob)


def common_clean(
    df: pd.DataFrame,
    dropna: str = "any",
    tz: str = "Europe/Bucharest",
) -> pd.DataFrame:
    df = df.tz_convert(tz)
    df = df.tz_localize(None)

    if dropna:
        df.dropna(how=dropna, inplace=True)
    df = df.reindex(columns=["open", "high", "low", "close", "volume"])

    return df
