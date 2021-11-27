from os import environ
from datetime import datetime, timedelta
from typing import Tuple, List, Optional, Type
from types import TracebackType
import pandas as pd
from binance import Client
from . import common_clean


BINANCE_PARAMS = {
    "symbol": "BNBBTC",
    "interval": "1h",
    "start_str": str(datetime.timestamp(datetime.now() - timedelta(days=120))),
    "end_str": str(datetime.timestamp(datetime.now())),
}


class BinanceContext(object):
    def download(self, **kwargs) -> List:
        return self.client.get_historical_klines(**kwargs)

    def __enter__(self) -> "BinanceContext":
        self.client = Client(
            api_key=environ.get("BINANCE_API_KEY"),
            api_secret=environ.get("BINANCE_API_SECRET"),
        )
        return self

    def __exit__(
        self,
        exec_type: Optional[Type[BaseException]],
        exec_val: Optional[BaseException],
        exec_tb: Optional[TracebackType],
    ) -> bool:
        if not exec_tb:
            self.client.close_connection()
        else:
            print(f"Binance forced exit reason: {exec_type}, {exec_val}, {exec_tb}")
        return False


def extract(binance: BinanceContext, **kwargs) -> Tuple[List, str]:
    data = binance.download(**kwargs)
    return data, kwargs["symbol"]


def clean(data: List) -> pd.DataFrame:
    df = pd.DataFrame(
        [
            {
                "datetime": str(elem[0]),
                "open": float(elem[1]),
                "high": float(elem[2]),
                "low": float(elem[3]),
                "close": float(elem[4]),
                "volume": int(float(elem[5])),
            }
            for elem in data
        ]
    )

    df.set_index("datetime", inplace=True)
    df.index = pd.to_datetime(df.index, unit="ms")
    df.index = df.index.tz_localize("UTC")

    return common_clean(df)
