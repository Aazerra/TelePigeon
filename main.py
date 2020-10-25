import os

from telebot import apihelper
from telebot.types import Message

from bot import Bot
from config import Config
from models.user import AnonymousUser
from storage.redis import RedisStorage
import i18n

# https://api.telegram.org/

i18n.load_path.append(os.path.join(os.getcwd(), "locales"))
i18n.set('file_format', 'json')
i18n.set('locale', 'fa')
i18n.set("available_locales", ["en", "fa"])
i18n.set('skip_locale_root_data', True)

apihelper.ENABLE_MIDDLEWARE = True

config = Config()
storage = RedisStorage(db=5)
storage.set_admin(config.sudo)
bot = Bot(config.token, storage)
admin = bot.storage.get_admin()


@bot.middleware_handler(update_types=['message'])
def message_middleware(context, message):
    user = context.storage.get_user(message.from_user.id)
    if isinstance(user, AnonymousUser):
        user = context.storage.register_user(
            message.from_user.id, message.from_user)
    message.user = user


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, bot.t("messages.welcome", username=bot.me.username))


@bot.message_handler(content_types=['video', "video_note", "photo", "animation", "document", "sticker", "voice"],
                     func=lambda m: not m.user.is_admin)
def file_member(message: Message):
    sent = bot.forward_message(admin, message.chat.id, message.message_id)
    bot.storage.save_message_id(sent.message_id, message.from_user.id)
    bot.reply_to(message, bot.t("messages.sent.user"))


@bot.message_handler(content_types=['video', "video_note", "photo", "animation", "document", "sticker", "voice"],
                     func=lambda m: m.user.is_admin)
def files_admin(message: Message):
    if not message.reply_to_message:
        return
    if message.content_type == "document" and message.animation:
        message.content_type = "animation"
    message_id = message.reply_to_message.message_id
    content_type = message.content_type
    user_id = bot.storage.get_message_info(message_id)
    file = bot.get_file_from_message(message)
    bot.__getattribute__(f"send_{content_type}")(user_id, file.file_id)


@bot.message_handler(content_types=['text'], func=lambda m: not m.user.is_admin)
def text(message: Message):
    sent = bot.forward_message(admin, message.chat.id, message.message_id)
    bot.storage.save_message_id(sent.message_id, message.from_user.id)
    bot.reply_to(message, bot.t("messages.sent.user"))


@bot.message_handler(content_types=['text'], func=lambda m: m.user.is_admin)
def text_admin(message: Message):
    if not message.reply_to_message:
        return
    message_id = message.reply_to_message.message_id
    user_id = bot.storage.get_message_info(message_id)
    bot.send_message(user_id, message.text)
    bot.reply_to(message, bot.t("messages.sent.admin"))


if __name__ == '__main__':
    bot.polling()
