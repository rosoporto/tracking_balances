import requests


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


if __name__ == "__main__":
    loader = WebContentLoader()


# TODO:
# A. Добавить возможность задания заголовков (headers) для запроса
# B. Добавить метод для сохранения контента в файл
# C. Расширить класс для поддержки POST запросов
# D. Реализовать обработку различных типов контента (JSON, XML и т.д.)
