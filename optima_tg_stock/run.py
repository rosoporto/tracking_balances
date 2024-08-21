from .config.settings import Settings
from .modules.DataModule import DataModule
from .modules.WebContentParser import WebContentLoader, WebContentParser
from .modules.custom_logging import Logger
from .modules.bot import TelegramBot


def main():
    settings = Settings()
    logger = Logger(settings.filename_to_log)

    content_loader = WebContentLoader(logger)
    data_max: str = WebContentParser(content_loader, logger)

    telegram_token = settings.telegram_token
    telegram_user_id = int(settings.telegram_user_id)

    data_module = DataModule(settings, data_max)
    bot = TelegramBot(telegram_token, [telegram_user_id], data_module)
    bot.run()


if __name__ == "__main__":
    main()
