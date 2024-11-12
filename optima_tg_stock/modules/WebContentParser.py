from bs4 import BeautifulSoup
from .WebContentLoader import WebContentLoader
from .load_json import load_products_from_json
from .custom_logging import Logger
from ..config.settings import Settings


class WebContentParser:
    def __init__(self, content_loader, logger):
        self.content_loader = content_loader
        self.content = None
        self.soup = None
        self.logger = logger

    def load_and_parse_content(self, url):
        self.content = self.content_loader.load_content(url)
        self.soup = self.parse_content()

    def parse_content(self):
        if self.content:
            return BeautifulSoup(self.content, 'lxml')
        else:
            return None

    def get_stock(self):
        try:
            if self.soup:
                data_max = self.soup.find('span', {'class': 'plus'})['data-max']
                return data_max
            else:
                return 0
        except Exception as e:
            self.logger.error(f"Error extracting data-max: {e}")
            raise ValueError("Ошибка при извлечении данных")
        finally:
            self.content = None
            self.soup = None

def main():
    settings = Settings()
    logger = Logger(settings.path_to_log)
    content_loader = WebContentLoader(logger)
    parser = WebContentParser(content_loader, logger)

    products = load_products_from_json(settings.data_file_path)

    for product_name, url in products.items():
        parser.load_and_parse_content(url)
        print(f'{product_name}: {parser.get_stock()} шт.')


if __name__ == "__main__":
    main()
