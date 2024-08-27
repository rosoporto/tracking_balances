import os
import logging
from ..config.settings import Settings
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, filename_to_log, log_level=logging.DEBUG):
        # Проверка на существование файла и его создание, если он отсутствует
        if not os.path.exists(filename_to_log):
            open(filename_to_log, 'w').close()  # Создаем пустой файл

        # Настройка обработчика ротации файлов
        handler = RotatingFileHandler(
            filename=filename_to_log,
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(funcName)s')
        handler.setFormatter(formatter)

        # Настройка логирования
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)  # Установка уровня логирования
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    settings = Settings()
    log = Logger(settings.path_to_log, log_level=logging.INFO)
    log.debug('Это отладочное сообщение.')
    log.info('Это информационное сообщение.')
    log.warning('Это предупреждающее сообщение.')
    log.error('Это сообщение об ошибке.')
    log.critical('Это критическое сообщение.')
