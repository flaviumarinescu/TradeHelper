from datetime import datetime, timedelta
import redis
from huey import crontab, SqliteHuey
from pipelines import load, binance_candles, yahoo_candles
from binance.exceptions import BinanceAPIException, BinanceRequestException

huey = SqliteHuey(
    filename="/tmp/huey.db",
)

cache = redis.Redis(
    **{
        "host": "cache",
        "db": 0,
        "charset": "utf-8",
        "port": 6379,
    }
)


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
    """Downloads OHLCV asset data from yahoo finance"""
    with open("assets") as f:
        assets = [
            {
                "tickers": line.rstrip().split(",")[0],
                "start": datetime.now() - timedelta(days=120),
                "end": datetime.now(),
            }
            for line in f
            if not line.isspace()
            and not line.startswith("##")
            and line.rstrip().split(",")[1] == "yahoo"
        ]

    for asset in assets:
        kwargs = {**yahoo_candles.YF_PARAMS, **asset}
        try:
            df, ticker = yahoo_candles.extract(**kwargs)
            df = yahoo_candles.clean(df)
            cache.ping()  # Check cache availability
        except redis.exceptions.ConnectionError as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to connect with redis {e}"
            )
        except Exception as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {asset['tickers']} processing from yahoo failed: {e}"
            )
        else:
            load(df, ticker, cache)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {ticker} successfully processed"
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
    """Downloads OHLCV asset data from binance"""
    with open("assets") as f:
        assets = [
            {
                "symbol": line.rstrip().split(",")[0].upper(),
                "start_str": str(
                    datetime.timestamp(datetime.now() - timedelta(days=120))
                ),
                "end_str": str(datetime.timestamp(datetime.now())),
            }
            for line in f
            if not line.isspace()
            and not line.startswith("##")
            and line.rstrip().split(",")[1] == "binance"
        ]

    with binance_candles.BinanceContext() as binance:
        for asset in assets:
            kwargs = {**binance_candles.BINANCE_PARAMS, **asset}
            try:
                df, ticker = binance_candles.extract(binance, **kwargs)
                df = binance_candles.clean(df)
                cache.ping()
            except redis.exceptions.ConnectionError as e:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to connect with redis {e}"
                )
            except (BinanceAPIException, BinanceRequestException) as e:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {asset['tickers']} download from binance failed: {e}"
                )
            except Exception as e:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {asset['tickers']} processing from binance failed: {e}"
                )
            else:
                load(df, ticker, cache)
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {ticker} successfully processed"
                )
