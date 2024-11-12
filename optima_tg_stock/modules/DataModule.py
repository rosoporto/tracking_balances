import os
import json
from .custom_logging import Logger
from .WebContentParser import WebContentParser
from .WebContentLoader import WebContentLoader
from ..config.settings import Settings


class DataModule:
    """
    Returns a json file with product details in the form product: balance
    """
    def __init__(self, data_file_path, logger):
        self.data_file_path: str = data_file_path
        self.logger: Logger = logger
        self.content_loader = WebContentLoader(self.logger)

    def process_data(self):
        try:
            data = self.load_data(self.data_file_path)
        except FileNotFoundError as error_answer:
            self.logger.error(error_answer)
            return None

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
            raise FileNotFoundError(f"Файл '{data_file_path}' не найден.")

        with open(data_file_path, "r") as file:
            data = json.load(file)
        return data


def main():
    settings = Settings()
    logger = Logger(settings.path_to_log)

    data_module = DataModule(
        settings.data_file_path,
        logger
    )
    result = data_module.process_data()
    print(result)


if __name__ == '__main__':
    main()
