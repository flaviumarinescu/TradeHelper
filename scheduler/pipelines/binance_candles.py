"""
    Pipeline functionality for binance.
"""

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


class BinanceContext:
    """Creates a context for establishing a connection with binance API."""

    def __init__(self, api_key: str = None, api_secret: str = None):
        """Constructor for BinanceContext

        Args:
            api_key (str, optional): Binance API Key. Defaults to None.
                If left blank, BINANCE_API_KEY environment variable needs to be set.
            api_secret (str, optional): Binance API Secret. Defaults to None.
                If left blank, BINANCE_API_SECRET environment variable needs to be set.
        """
        self.client = None
        self.api_key = api_key if api_key else environ.get("BINANCE_API_KEY")
        self.api_secret = (
            api_secret if api_secret else environ.get("BINANCE_API_SECRET")
        )

    def download(self, **kwargs) -> List:
        """Downloads raw data from binance.

        Returns:
            List: Data is returned as a list of lists.
                Example:
                [
                    [
                        1499040000000,      // Open time
                        "0.01634790",       // Open
                        "0.80000000",       // High
                        "0.01575800",       // Low
                        "0.01577100",       // Close
                        "148976.11427815",  // Volume
                        1499644799999,      // Close time
                        "2434.19055334",    // Quote asset volume
                        308,                // Number of trades
                        "1756.87402397",    // Taker buy base asset volume
                        "28.46694368",      // Taker buy quote asset volume
                        "17928899.62484339" // Ignore
                    ],
                ]
        """
        return self.client.get_historical_klines(**kwargs)

    def __enter__(self) -> "BinanceContext":
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
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


def extract(binance: BinanceContext, **kwargs: BINANCE_PARAMS) -> Tuple[List, str]:
    """Extracts data from binance API.

    Args:
        binance (BinanceContext): Requires a binance context to extract data.

    Returns:
        Tuple[List, str]: Returns raw data and ticker symbol.
    """
    data = binance.download(**kwargs)
    return data, kwargs["symbol"]


def clean(data: List) -> pd.DataFrame:
    """Cleans extracted data from binance.

    Args:
        data (List): Raw data from the above, extract, function.

    Returns:
        pd.DataFrame: Processed, ready to use, dataframe.
            * Check for final intended format in __init__.py, common_clean()
    """
    dataframe = pd.DataFrame(
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

    dataframe.set_index("datetime", inplace=True)
    dataframe.index = pd.to_datetime(dataframe.index, unit="ms")
    dataframe.index = dataframe.index.tz_localize("UTC")

    return common_clean(dataframe)
