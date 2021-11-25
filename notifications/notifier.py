from multiprocessing import Process
from providers import Telegram, NotificationProvider
import redis
from datetime import datetime

cache = redis.Redis(
    **{
        "host": "cache",
        "db": 0,
        "charset": "utf-8",
        "port": 6379,
    }
)


def subscriber(channel: str, provider: NotificationProvider) -> None:
    comm = provider()
    pubsub = cache.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message.get("type") == "message":
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message : {message}"
            )
            data = message.get("data")
            comm.send_text(data)


if __name__ == "__main__":
    Process(target=subscriber, args=("notify", Telegram)).start()
