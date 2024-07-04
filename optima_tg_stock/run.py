from .config.settings import Settings
from .modules.DataModule import DataModule
from .modules.WebContentParser import WebContentLoader, WebContentParser


def main():
    settings = Settings()
    loader = WebContentLoader()
    parser = WebContentParser(loader)

    data_module = DataModule(settings, parser)
    result = data_module.get_data()
    print(result)


if __name__ == "__main__":
    main()
