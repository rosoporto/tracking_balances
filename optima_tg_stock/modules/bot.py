import time
import pytz
import datetime
import schedule
from .custom_logging import Logger
from .ContentManager import ContentManager
from ..config.settings import Settings
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


class TelegramBot:
    def __init__(self, settings, logger):
        self.settings = settings
        self.allowed_users = list(map(int, self.settings.telegram_user_id.split(",")))
        self.logger = logger
        self.content_manager = ContentManager(
            self.settings.data_file_path,
            self.settings.min_stock_quantity,
            self.logger
        )
        self.auth_user = False
        self.start_message_id = None
        self.updater = Updater(self.settings.telegram_token, use_context=True)
        self.dp = self.updater.dispatcher

        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(CommandHandler('stop', self.stop))
        self.dp.add_handler(CallbackQueryHandler(self.button))

    def start(self, update, context):
        if update.effective_user.id in self.allowed_users:
            user = self.get_username(update.effective_user.id, context)
            self.logger.info(f"Бот для юзера @{user} запущен")

            self.auth_user = True
            keyboard = [[InlineKeyboardButton('Stop', callback_data='stop')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.callback_query:
                update.callback_query.edit_message_text('Бот запущен!', reply_markup=reply_markup)
            else:
                # Сохраняем идентификатор стартового сообщения
                start_message = update.message.reply_text('Бот запущен!', reply_markup=reply_markup, quote=True)
                self.start_message_id = start_message.message_id  # Сохраняем идентификатор

            time_to_sent = self.settings.run_time
            schedule.every().day.at(time_to_sent).do(self.job, context)

            # Удаляем кнопки через некоторое время
            context.job_queue.run_once(self.remove_buttons, 86400, context=update.effective_chat.id)

        else:
            self.logger.info(f"Неавторизованный пользователь: {update.effective_user.id}")
            update.message.reply_text('У вас нет доступа к этому боту.', quote=True)

    def remove_buttons(self, context):
        chat_id = context.job.context
        if self.start_message_id:
            try:
                context.bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=self.start_message_id,
                    reply_markup=None
                )
            except Exception as e:
                self.logger.error(f"Ошибка при удалении кнопок: {e}")

    def stop(self, update, context):
        if update.effective_user.id in self.allowed_users:
            self.auth_user = False
            keyboard = [[InlineKeyboardButton('Start', callback_data='start')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.callback_query:
                update.callback_query.edit_message_text('Бот остановлен!', reply_markup=reply_markup)
            else:
                update.message.reply_text('Бот остановлен!', reply_markup=reply_markup)
            user = self.get_username(update.effective_user.id, context)
            self.logger.info(f"Бот для юзера @{user} остановлен")
        else:
            if update.callback_query:
                update.callback_query.edit_message_text('У вас нет доступа к этому боту.')

    def button(self, update, context):
        query = update.callback_query
        if query.data == 'start':
            self.start(update, context)
        elif query.data == 'stop':
            self.stop(update, context)

    def get_username(self, user_id, context):
        try:
            user = context.bot.get_chat_member(chat_id=user_id, user_id=user_id).user
            username = user.username if user.username else f"{user_id}"
            return username
        except Exception as e:
            self.logger.error(f"Ошибка получения имени пользователя: {e}")
            return str(user_id)

    def send_messages(self, context):
        if self.auth_user:
            self.logger.info("Процесс сбора данных начался")
            message = self.content_manager.create_answer()

            if message is None:
                # Если товаров достаточно, отправляем сообщение пользователю
                for user_id in self.allowed_users:
                    try:
                        context.bot.send_message(chat_id=user_id, text="Товары в достаточном количестве.")
                    except Exception as e:
                        self.logger.error(f"Ошибка {e} отправки сообщения пользователю {user_id}")
                self.send_control_buttons(context)  # Отправляем кнопки
                return  # Выходим из метода, так как нет необходимости отправлять остатки

            for user_id in self.allowed_users:
                try:
                    context.bot.send_message(chat_id=user_id, text=message)
                except Exception as e:
                    self.logger.error(f"Ошибка {e} отправки сообщения пользователю {user_id}")

            self.logger.info("Остатки доставлены")
            self.send_control_buttons(context)  # Отправляем кнопки

    def send_control_buttons(self, context):
        if self.auth_user:
            keyboard = [
                [InlineKeyboardButton('Stop', callback_data='stop')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message_text = "Бот работает. Выберите действие:"
        else:
            keyboard = [
                [InlineKeyboardButton('Start', callback_data='start')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message_text = "Бот остановлен. Выберите действие:"

        for user_id in self.allowed_users:
            try:
                context.bot.send_message(chat_id=user_id, text=message_text, reply_markup=reply_markup)
            except Exception as e:
                self.logger.error(f"Ошибка отправки кнопок пользователю {user_id}: {e}")

    def job(self, context):
        now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        days_off = self.settings.days_off
        if days_off:
            days_off = [int(day) for day in days_off.split(',')]
        else:
            days_off = []
        if now.weekday() not in days_off:
            self.send_messages(context)

    def run(self):
        self.updater.start_polling()
        while True:
            schedule.run_pending()
            time.sleep(1)
        self.updater.idle()


if __name__ == '__main__':
    settings = Settings()
    logger = Logger(settings.path_to_log)  # Передаем путь к логам
    bot = TelegramBot(settings, logger)
    bot.run()

# TODO:
# schedule.every(3).minutes.do(job)  # запуск функции каждые 3 минуты
