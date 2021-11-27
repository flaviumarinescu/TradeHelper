from abc import ABC, abstractmethod
from os import environ
import telebot


class NotificationProvider(ABC):
    @abstractmethod
    def send_text(self, message: str) -> None:
        pass

    @abstractmethod
    def send_image(self, image) -> None:
        pass


class Telegram(NotificationProvider):
    def __init__(self):
        self._bot = telebot.TeleBot(
            token=environ.get("TELEGRAM_TOKEN"), parse_mode=None
        )
        self._chat_id = environ.get("TELEGRAM_CHAT_ID")

    def send_text(self, message: str) -> None:
        if message:
            self._bot.send_message(self._chat_id, message, parse_mode=None)

    def send_image(self, image) -> None:
        raise NotImplementedError
