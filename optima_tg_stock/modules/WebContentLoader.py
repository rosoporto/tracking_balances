import requests
from .custom_logging import Logger
from .load_json import load_products_from_json
from ..config.settings import Settings


class WebContentLoader:
    def __init__(self, logger, user_agent='Mozilla/5.0'):
        self.user_agent = user_agent
        self.headers = {'User-Agent': self.user_agent}
        self.logger = logger

    def load_content(self, url):
        self.logger.info(f"Attempting to fetch content from {url}")
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            self.logger.info(f"Successfully fetched content from {url}")
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None


if __name__ == "__main__":
    settings = Settings()
    logger = Logger(settings.path_to_log)
    loader = WebContentLoader(logger)

    products = load_products_from_json(settings.data_file_path)

    for product_name, url in products.items():
        logger.info(f"Processing product: {product_name}")
        content = loader.load_content(url)
        if content:
            print(f"Content loaded for product: {product_name}")
        else:
            logger.warning(f"Failed to load content for product: {product_name}")


# TODO:
# A. Добавить возможность задания заголовков (headers) для запроса
# B. Добавить метод для сохранения контента в файл
# C. Расширить класс для поддержки POST запросов
# D. Реализовать обработку различных типов контента (JSON, XML и т.д.)
