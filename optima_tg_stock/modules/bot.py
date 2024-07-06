import schedule
import time
import pytz
import datetime
import logging
from ..config.settings import Settings
from .WebContentParser import WebContentParser
from .WebContentLoader import WebContentLoader
from .DataModule import DataModule
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, token, allowed_users, data_module):
        self.token = token
        self.allowed_users = allowed_users
        self.auth_user = False
        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher
        self.data_module = data_module
        self.sent_messages = {}
        self.max_sent_messages = 10

        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(CommandHandler('stop', self.stop))
        self.dp.add_handler(CallbackQueryHandler(self.button))

    def start(self, update, context):
        if update.effective_user.id in self.allowed_users:
            user = self.get_username(update.effective_user.id, context)
            logger.info("Бот для юзера @%s запущен", user)

            self.auth_user = True
            keyboard = [[InlineKeyboardButton('Stop', callback_data='Stop')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.callback_query:
                update.callback_query.edit_message_text('Бот запущен!', reply_markup=reply_markup)
            else:
                update.message.reply_text('Бот запущен!', reply_markup=reply_markup, quote=True)
            schedule.every().day.at("10:00").do(self.job, context)            
        else:
            logger.info("Неавторизованный пользователь : %s", update.effective_user.id)
            update.message.reply_text('У вас нет доступа к этому боту.', quote=True)            

    def stop(self, update, context):
        if update.effective_user.id in self.allowed_users:
            self.auth_user = False
            keyboard = [[InlineKeyboardButton('Start', callback_data='start')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.callback_query.edit_message_text(
                'Бот остановлен!',
                reply_markup=reply_markup
            )
            user = self.get_username(update.effective_user.id, context)
            logger.info("Бот для юзера @%s остановлен", user)
        else:
            update.callback_query.edit_message_text(
                'У вас нет доступа к этому боту.'
            )

    def button(self, update, context):
        query = update.callback_query
        if query.data == 'start':
            self.start(update, context)
        elif query.data == 'stop':
            self.stop(update, context)

    def get_username(self, user_id, context):
        user = context.bot.get_chat_member(chat_id=user_id, user_id=user_id).user
        username = user.username if user.username else f"{user_id}"
        return username

    def send_messages(self, context):
        if self.auth_user:
            logger.info("Процесс сбора данных начался")
            result = self.data_module.process_data()
            for user_id in self.allowed_users:
                context.bot.send_message(chat_id=user_id, text=result)
            logger.info("Остатки доставлены")
            # Добавить кнопку "Стоп"
            keyboard = [[InlineKeyboardButton('Stop', callback_data='stop')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            for user_id in self.allowed_users:
                context.bot.send_message(
                    chat_id=user_id,
                    text="Остатки переданы!",
                    reply_markup=reply_markup
                )

    def job(self, context):
        now = datetime.now(pytz.timezone('Europe/Moscow'))
        if now.weekday() not in [5, 6]:  # 5 - Saturday, 6 - Sunday
            self.send_messages(context)

    def run(self):
        self.updater.start_polling()
        while True:
            schedule.run_pending()
            time.sleep(1)
        self.updater.idle()


if __name__ == '__main__':
    settings = Settings()
    telegram_token = settings.telegram_token
    telegram_user_id = settings.telegram_user_id

    loader = WebContentLoader()
    parser = WebContentParser(loader)

    data_module = DataModule(settings, parser)

    bot = TelegramBot(telegram_token, [telegram_user_id], data_module)
    bot.run()


# TODO:
# schedule.every(3).minutes.do(job)  # запуск функции каждые 3 минуты
