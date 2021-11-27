"""Functions that are shared by multiple pipelines"""

from typing import Any
import pickle
import pandas as pd
import redis


def load(obj: Any, key: str, cache: redis.Redis) -> bool:
    """Stores any pickleable python  object inside a redis instance.

    Args:
        obj (Any): Any python object.
        key (str): Key for telling redis where to store object.
        cache (redis.Redis): Redis connection.

    Returns:
        bool:  True if successfully stored object, False otherwise.
    """
    pickeld_ob = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    return cache.set(key, pickeld_ob)


def common_clean(
    df: pd.DataFrame,
    dropna: str = "any",
    timezone: str = "Europe/Bucharest",
) -> pd.DataFrame:
    """Common data cleaning steps.

    Args:
        df (pd.DataFrame): Pandas dataframe with open high low close columns and datetime index
        dropna (str, optional): Removes any Nan values from dataframe. Defaults to "any".
        timezone (str, optional): Switches timezone to this values. Defaults to "Europe/Bucharest".

    Returns:
        pd.DataFrame: Returns processed dataframe.
    """
    df = df.tz_convert(timezone)
    df = df.tz_localize(None)

    if dropna:
        df.dropna(how=dropna, inplace=True)
    df = df.reindex(columns=["open", "high", "low", "close", "volume"])

    return df
