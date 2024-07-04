import json
from ..config.settings import Settings
from .WebContentParser import WebContentParser
from .WebContentLoader import WebContentLoader


class DataModule:
    def __init__(self, settings, parser):
        self.settings = settings
        self.parser = parser

    def get_data(self):
        data_file_path = self.settings.data_file_path
        data = self.load_data(data_file_path)
        products = data["products"]
        result = []
        for product, url in products.items():
            self.parser.load_and_parse_content(url)
            stock = self.parser.get_stock()

            stock_product = ''
            if stock:
                stock_product = f'{product}: осталось {stock} штук'
            else:
                stock_product = f'Для {product} не удалось получить остатки.'
            result.append(stock_product)

        return '\n'.join(result)

    def load_data(self, data_file_path):
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
