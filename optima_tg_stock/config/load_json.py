import json
from .settings import Settings


def load_data(data_file_path):
    with open(data_file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == '__main__':
    settings = Settings()
    data_file_path = settings.data_file_path
    data = load_data(data_file_path)
    products = data["products"]

    for product, url in products.items():
        print(product, url)
