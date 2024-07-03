from .config.settings import Settings
from .config.load_json import load_data
from .modules.content_processing import WebContentLoader, WebContentParser


def main():
    settings = Settings()
    data_file_path = settings.data_file_path

    data = load_data(data_file_path)
    products = data["products"]

    loader = WebContentLoader()
    for product, url in products.items():
        content = loader.load_content(url)
        if content:
            parser = WebContentParser(content)
            data = parser.get_stock()
            if data:
                print(data)
            else:
                print("Не удалось получить контент страницы.")
        else:
            print("Не удалось получить контент страницы.")


if __name__ == "__main__":
    main()
