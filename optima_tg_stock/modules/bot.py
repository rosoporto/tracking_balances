import schedule
import time
import pytz
import datetime
from ..config.settings import Settings
from .WebContentParser import WebContentParser
from .WebContentLoader import WebContentLoader
from .DataModule import DataModule
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

class TelegramBot:
    def __init__(self, token, allowed_users, data_module):
        self.token = token
        self.allowed_users = allowed_users
        self.send_messages = False
        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher
        self.data_module = data_module

        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(CommandHandler('stop', self.stop))
        self.dp.add_handler(CallbackQueryHandler(self.button))        

    def start(self, update, context):
        if update.effective_user.id in self.allowed_users:
            self.send_messages = True
            keyboard = [[InlineKeyboardButton('Stop', callback_data='stop')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Бот запущен!', reply_markup=reply_markup)
            
            # Отправлять сообщения каждый день в 10:00 по московскому времени
            schedule.every().day.at("10:00").do(self.job, context)
        else:
            update.message.reply_text('У вас нет доступа к этому боту.')

    def stop(self, update, context):
        if update.effective_user.id in self.allowed_users:
            self.send_messages = False
            keyboard = [[InlineKeyboardButton('Start', callback_data='start')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Бот остановлен!', reply_markup=reply_markup)
        else:
            update.message.reply_text('У вас нет доступа к этому боту.')

    def button(self, update, context):
        query = update.callback_query
        if query.data == 'start':
            self.start(update, context)
        elif query.data == 'stop':
            self.stop(update, context)

    def send_messages(self, context):
        if self.send_messages:
            data = self.data_module.get_data()
            for user_id in self.allowed_users:
                context.bot.send_message(chat_id=user_id, text=data)

    def job(self, context):
        now = datetime.now(pytz.timezone('Europe/Moscow'))
        if now.weekday() not in [5, 6]:  # 5 - Saturday, 6 - Sunday
            self.send_messages(context)

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    data_module = DataModule()  # Создаем экземпляр модуля данных
    
    settings = Settings()
    telegram_token = settings.telegram_token
    telegram_user_id = settings.telegram_user_id
    
    loader = WebContentLoader()
    parser = WebContentParser(loader)

    data_module = DataModule(settings, parser)
    
    bot = TelegramBot(telegram_token, [telegram_user_id], data_module)
    bot.run()
