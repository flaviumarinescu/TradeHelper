from huey import crontab, SqliteHuey
import redis
from pipelines.yahoo_market_data import extract, clean, load, YF_PARAMS
from datetime import datetime, timedelta


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
        day_of_week="*",
        hour="*",
        minute="3",
    ),
    # retries=2,
    # retry_delay=30,
)
def yahoo_market_data_pipeline() -> None:

    with open("assets") as f:
        assets = [
            {
                "tickers": line.rstrip(),
                "start": datetime.now() - timedelta(days=120),
                "end": datetime.now(),
            }
            for line in f
            if not line.isspace() and not line.startswith("##")
        ]

    for asset in assets:
        params = {**YF_PARAMS, **asset}
        try:
            df, ticker = extract(**params)
            df = clean(df)
            cache.ping()  # Check cache availability
        except redis.exceptions.ConnectionError as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to connect with redis {e}"
            )
        except Exception as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {asset['tickers']} processing failed: {e}"
            )
        else:
            load(df, ticker, cache)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {ticker} successfully processed"
            )
