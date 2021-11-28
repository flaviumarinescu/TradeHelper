"""
    Functionalities shared by multiple pipelines.
"""

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
    dataframe: pd.DataFrame,
    dropna: str = "any",
    timezone: str = "Europe/Bucharest",
) -> pd.DataFrame:
    """Common data cleaning steps.

    Args:
        dataframe (pd.DataFrame): Dataframe with open high low close columns and datetime index
        dropna (str, optional): Removes any Nan values from dataframe. Defaults to "any".
        timezone (str, optional): Switches timezone to this values. Defaults to "Europe/Bucharest".

    Returns:
        pd.DataFrame: Returns processed dataframe.

            The following format should be wanted after running specific pipeline clean function
            and the common clean.

                                    open     high      low    close      volume
            datetime
            2021-09-13 09:00:00  0.02103  0.07805  0.02103  0.06577  1431698394
    """
    dataframe = dataframe.tz_convert(timezone)
    dataframe = dataframe.tz_localize(None)

    if dropna:
        dataframe.dropna(how=dropna, inplace=True)
    dataframe = dataframe.reindex(columns=["open", "high", "low", "close", "volume"])

    return dataframe
