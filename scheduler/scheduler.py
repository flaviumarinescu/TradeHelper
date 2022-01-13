"""
    Tasks to be scheduled by the huey consumer.
"""

from datetime import datetime, timedelta
from os import environ
import redis
from huey import crontab, SqliteHuey
from binance.exceptions import BinanceAPIException, BinanceRequestException
from pipelines import load, binance_candles, yahoo_candles


huey = SqliteHuey(
    filename=environ.get("HUEY_DB"),
)

cache = redis.Redis(host="cache")


@huey.periodic_task(
    crontab(
        month="*",
        day="*",
        day_of_week="1-5",
        hour="*",
        minute="3",
    ),
)
def yahoo_candles_pipeline() -> None:
    """
    Downloads OHLCV asset data from yahoo finance,
    Transforms data and stores it into cache. Acts as and ETL Pipeline.
    """
    with open("assets", encoding="UTF-8") as file:
        assets = [
            {
                "tickers": line.rstrip().split(",")[0],
                "start": datetime.now() - timedelta(days=120),
                "end": datetime.now(),
            }
            for line in file
            if not line.isspace()
            and not line.startswith("##")
            and line.rstrip().split(",")[1] == "yahoo"
        ]

    for asset in assets:
        kwargs = {**yahoo_candles.YF_PARAMS, **asset}
        try:
            dataframe, ticker = yahoo_candles.extract(**kwargs)
            dataframe = yahoo_candles.clean(dataframe)
            cache.ping()  # Check cache availability
        except redis.exceptions.ConnectionError as err:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Failed to connect with redis {err}"
            )
        except (Exception,) as err:  # pylint: disable=broad-except
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{asset['tickers']} processing from yahoo failed: {err}"
            )
        else:
            load(dataframe, ticker, cache)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{ticker} successfully processed"
            )


@huey.periodic_task(
    crontab(
        month="*",
        day="*",
        day_of_week="*",
        hour="*",
        minute="0",
    ),
)
def binance_candles_pipeline() -> None:
    """
    Downloads OHLCV asset data from binance,
    Transforms data and stores it into cache. Acts as and ETL Pipeline.
    """
    with open("assets", encoding="UTF-8") as file:
        assets = [
            {
                "symbol": line.rstrip().split(",")[0].upper(),
                "start_str": str(
                    datetime.timestamp(datetime.now() - timedelta(days=120))
                ),
                "end_str": str(datetime.timestamp(datetime.now())),
            }
            for line in file
            if not line.isspace()
            and not line.startswith("##")
            and line.rstrip().split(",")[1] == "binance"
        ]

    with binance_candles.BinanceContext() as binance:
        for asset in assets:
            kwargs = {**binance_candles.BINANCE_PARAMS, **asset}
            try:
                dataframe, ticker = binance_candles.extract(binance, **kwargs)
                dataframe = binance_candles.clean(dataframe)
                cache.ping()
            except redis.exceptions.ConnectionError as err:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Failed to connect with redis {err}"
                )
            except (BinanceAPIException, BinanceRequestException) as err:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{asset['tickers']} download from binance failed: {err}"
                )
            except (Exception,) as err:  # pylint: disable=broad-except
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{asset['tickers']} processing from binance failed: {err}"
                )
            else:
                load(dataframe, ticker, cache)
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{ticker} successfully processed"
                )
