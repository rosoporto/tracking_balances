import unittest
from unittest.mock import MagicMock, patch
from optima_tg_stock.modules.bot import TelegramBot  # Импортируйте ваш класс бота


class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        # Инициализация бота с тестовыми настройками
        self.settings = MagicMock()
        self.settings.run_time = "00:00"  # Установите на время, которое будет тестироваться
        self.settings.days_off = "5,6"  # Пример выходных
        self.logger = MagicMock()
        self.bot = TelegramBot(self.settings, self.logger)

    @patch('optima_tg_stock.modules.bot.schedule.run_pending')  # Путь к schedule
    def test_job_sends_messages(self, mock_run_pending):
        # Настройка моков
        self.bot.auth_user = True
        self.bot.content_manager.create_answer = MagicMock(return_value="Test message")
        self.bot.allowed_users = [123456]  # Пример ID пользователя

        # Создание контекста
        mock_context = MagicMock()
        mock_context.bot.send_message = MagicMock()

        # Вызов метода job
        self.bot.job(mock_context)

        # Проверка, что сообщение было отправлено
        mock_context.bot.send_message.assert_called_with(chat_id=123456, text="Test message")

    @patch('optima_tg_stock.modules.bot.schedule.run_pending')  # Путь к schedule
    def test_job_does_not_send_messages_on_days_off(self, mock_run_pending):
        # Настройка моков
        self.bot.auth_user = True
        self.bot.settings.days_off = "0,1,2,3,4"  # Все дни рабочие
        self.bot.content_manager.create_answer = MagicMock(return_value="Test message")
        self.bot.allowed_users = [123456]

        # Создание контекста
        mock_context = MagicMock()

        # Вызов метода job
        self.bot.job(mock_context)

        # Проверка, что сообщение не было отправлено
        mock_context.bot.send_message.assert_not_called()


if __name__ == '__main__':
    unittest.main()
