from telebot import TeleBot
from telebot.types import Message

from storage import Storage
import i18n


class Bot(TeleBot):

    def __init__(self, token, storage: Storage, logger=None, config=None, **kwargs):
        super().__init__(token, **kwargs)
        self.logger = logger
        self.config = config
        self.storage = storage
        self.t = i18n.t

        self.me = self.get_me()
        print(f"Bot Username: {self.me.username}")

    @staticmethod
    def get_file_from_message(message: Message):
        content_type = message.content_type
        if content_type == "photo":
            return message.photo[-1]
        if content_type == "document" and message.animation:
            return message.animation
        return message.__getattribute__(content_type)
