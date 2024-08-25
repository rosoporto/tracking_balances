import unittest
from unittest.mock import MagicMock, patch
from optima_tg_stock.modules.bot import TelegramBot  # Импортируйте ваш класс бота


class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        # Инициализация бота с тестовыми настройками
        self.settings = MagicMock()
        self.settings.run_time = "21:30"  # Установите на время, которое будет тестироваться
        self.settings.days_off = "1,2"  # Пример выходных
        self.settings.telegram_token = "123456:ABCdefGHIjklMNOpqrSTUvwxYZ"  # Фейковый токен
        self.logger = MagicMock()
        self.bot = TelegramBot(self.settings, self.logger)

    @patch('optima_tg_stock.modules.bot.schedule.run_pending')  # Путь к schedule
    def test_job_does_not_send_messages_on_days_off(self, mock_run_pending):
        # Настройка моков
        self.bot.auth_user = True
        self.bot.content_manager.create_answer = MagicMock(return_value="Test message")
        self.bot.allowed_users = [123456]

        # Создание контекста
        mock_context = MagicMock()
        mock_context.bot.send_message = MagicMock()

        # Установите день недели на выходной (например, понедельник - 0, вторник - 1, ...).
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.weekday.return_value = 1  # Установите на выходной
            self.bot.job(mock_context)

        # Проверка, что сообщение не было отправлено
        mock_context.bot.send_message.assert_not_called()

    @patch('optima_tg_stock.modules.bot.schedule.run_pending')  # Путь к schedule
    def test_job_sends_messages(self, mock_run_pending):
        # Настройка моков
        self.bot.auth_user = True
        self.bot.content_manager.create_answer = MagicMock(return_value="Товары и остатки")
        self.bot.allowed_users = [123456]  # Пример ID пользователя

        # Создание контекста
        mock_context = MagicMock()
        mock_context.bot.send_message = MagicMock()

        # Установите день недели на рабочий (например, понедельник - 0, вторник - 1, ...).
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.weekday.return_value = 0  # Установите на рабочий день
            self.bot.job(mock_context)

        # Проверка, что send_message был вызван с любым текстом, содержащим "Товары"
        mock_context.bot.send_message.assert_any_call(chat_id=123456, text="Товары и остатки")

        # Проверка, что сообщение "Остатки переданы!" также было отправлено
        mock_context.bot.send_message.assert_any_call(chat_id=123456, text="Остатки переданы!")


if __name__ == '__main__':
    unittest.main()
