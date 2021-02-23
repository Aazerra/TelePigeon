import os

from telebot import apihelper
from telebot.types import Message

from bot import Bot
from config import Config
from models.user import AnonymousUser
from storage.redis import RedisStorage
import i18n

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


@bot.message_handler(
    content_types=['video', "video_note", "photo", "animation", "document", "sticker", "voice", "text"],
    func=lambda m: not m.user.is_admin)
def member_message_handler(message: Message):
    sent = bot.forward_message(admin, message.chat.id, message.message_id)
    bot.storage.save_message_id(sent.message_id, message.from_user.id)
    bot.reply_to(message, bot.t("messages.sent.user"))


@bot.message_handler(
    content_types=['video', "video_note", "photo", "animation", "document", "sticker", "voice", "text"],
    func=lambda m: m.user.is_admin)
def admin_message_handler(message: Message):
    if not message.reply_to_message:
        return
    message_id = message.reply_to_message.message_id
    user_id = bot.storage.get_message_info(message_id)
    bot.copy_message(user_id, message.chat.id, message.message_id)


if __name__ == '__main__':
    bot.polling()
