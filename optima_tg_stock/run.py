import logging
from .config.settings import Settings
from .modules.custom_logging import Logger
from .modules.bot import TelegramBot


def main():
    settings = Settings()

    logger = Logger(
        settings.path_to_log,
        log_level=logging.WARNING
    )

    bot = TelegramBot(settings, logger)
    bot.run()


if __name__ == "__main__":
    main()
