import json
from ..config.settings import Settings


def load_products_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data.get("products", {})


if __name__ == "__main__":
    settings = Settings()
    print(load_products_from_json(settings.data_file_path))
