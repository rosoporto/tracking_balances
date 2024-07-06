import os
import json
from ..config.settings import Settings
from .WebContentParser import WebContentParser
from .WebContentLoader import WebContentLoader


class DataModule:
    def __init__(self, settings, parser):
        self.settings = settings
        self.parser = parser        

    def process_data(self):
        data_file_path = self.settings.data_file_path
        try:
            data = self.load_data(data_file_path)
        except FileNotFoundError as e:
            return f"Ошибка: файл '{data_file_path}' не найден: {e}."

        products = data["products"]
        result = []
        for product, url in products.items():
            self.parser.load_and_parse_content(url)
            stock = self.parser.get_stock()

            stock_product = ''
            if stock is None:
                stock_product = f'Для {product} не удалось получить остатки.'

            if stock and self.check_stock():
                stock_product = f'ВНИМАНИЕ! {product}: осталось *{stock}* шт.'
            else:
                stock_product = f'{product}: {stock} шт.'
            result.append(stock_product)

        return '\n'.join(result)

    def check_stock(self):
        return True if self.settings.min_stock_quantity > 0 else False

    def load_data(self, data_file_path):
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f"File '{data_file_path}' not found.")

        with open(data_file_path, "r") as file:
            data = json.load(file)
        return data


if __name__ == '__main__':
    settings = Settings()
    loader = WebContentLoader()
    parser = WebContentParser(loader)

    data_module = DataModule(settings, parser)
    result = data_module.get_data()
    print(result)
