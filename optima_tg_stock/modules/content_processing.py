import requests
import lxml
from bs4 import BeautifulSoup


class WebContentLoader:
    def __init__(self, user_agent='Mozilla/5.0'):
        self.user_agent = user_agent
        self.headers = {'User-Agent': self.user_agent}

    def load_content(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None


class WebContentParser:
    def __init__(self, content, parser='lxml'):
        self.content = content
        self.parser = parser
        self.soup = self.parse_content()

    def parse_content(self):
        return BeautifulSoup(self.content, self.parser)

    def get_stock(self):
        try:
            data_max = self.soup.find('span', {'class': 'plus'})['data-max']
            return data_max
        except Exception as e:
            print(f"Error extracting data-max: {e}")
            return None


if __name__ == "__main__":
    loader = WebContentLoader()
    links = ['https://example.com', 'https://example.org']
    for link in links:
        content = loader.load_content(link)
        if content:
            parser = WebContentParser(content)
            data = parser.get_stock()
            if data:
                print(data)
            else:
                print("Не удалось получить контент страницы.")
        else:
            print("Не удалось получить контент страницы.")

# TODO:
# A. Добавить возможность задания заголовков (headers) для запроса
# B. Добавить метод для сохранения контента в файл
# C. Расширить класс для поддержки POST запросов
# D. Добавить метод для парсинга контента с помощью BeautifulSoup
# E. Реализовать обработку различных типов контента (JSON, XML и т.д.)
