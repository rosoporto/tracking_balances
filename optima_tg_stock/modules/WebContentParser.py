from bs4 import BeautifulSoup
from .WebContentLoader import WebContentLoader


class WebContentParser:
    def __init__(self, content_loader):
        self.content_loader = content_loader
        self.content = None
        self.soup = None

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
                return None
        except Exception as e:
            print(f"Error extracting data-max: {e}")
            return None


if __name__ == "__main__":
    urls = ['https://example.com', 'https://example.org']
    loader = WebContentLoader()
    parser = WebContentParser(loader)

    for url in urls:
        parser.load_and_parse_content(url)
        stock = parser.get_stock()
