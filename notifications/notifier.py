"""
    Module in charge of running subscriber function,
    that listens on a specifc channel and pushes messages to provider.
"""

from multiprocessing import Process
from datetime import datetime
from providers import Telegram, NotificationProvider
import redis


cache = redis.Redis(host="cache")


def subscriber(channel: str, provider: NotificationProvider) -> None:
    """Function that waits for data to be published from redis and reacts to messages.

    Args:
        channel (str): A redis subscriber channel
        provider (NotificationProvider): A class that has send_text method implemented.
    """
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
