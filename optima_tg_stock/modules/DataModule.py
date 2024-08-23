import os
import json
from .custom_logging import Logger
from .WebContentParser import WebContentParser
from .WebContentLoader import WebContentLoader
from ..config.settings import Settings


class DataModule:
    def __init__(self, data_file_path, logger):
        self.data_file_path: str = data_file_path        
        self.logger: Logger = logger
        self.content_loader = WebContentLoader(self.logger)

    def process_data(self):
        try:
            data = self.load_data(self.data_file_path)
        except FileNotFoundError as e:
            self.logger.error(f"Ошибка: файл '{self.data_file_path}' не найден: {e}")
            return f"Ошибка: файл '{self.data_file_path}' не найден: {e}."

        products = data["products"]
        result = {}
        parser = WebContentParser(self.content_loader, self.logger)
        for product, url in products.items():
            parser.load_and_parse_content(url)
            stock = parser.get_stock()
            result[product] = stock

        return result

    def load_data(self, data_file_path):
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f"File '{data_file_path}' not found.")

        with open(data_file_path, "r") as file:
            data = json.load(file)
        return data


if __name__ == '__main__':
    settings = Settings()
    logger = Logger(settings.path_to_log)

    data_module = DataModule(
        settings.data_file_path,
        logger
    )
    result = data_module.process_data()
    print(result)
