from .config.settings import Settings
from .modules.DataModule import DataModule
from .modules.WebContentParser import WebContentLoader, WebContentParser
from .modules.bot import TelegramBot


def main():
    settings = Settings()
    loader = WebContentLoader()
    parser = WebContentParser(loader)

    telegram_token = settings.telegram_token
    telegram_user_id = int(settings.telegram_user_id)    

    data_module = DataModule(settings, parser)
    bot = TelegramBot(telegram_token, [telegram_user_id], data_module)
    bot.run()


if __name__ == "__main__":
    main()
