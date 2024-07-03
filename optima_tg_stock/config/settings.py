import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()
        self.data_file_path = os.getenv("DATA_FILE_PATH")
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.telegram_user_id = os.getenv("TELEGRAM_USER_ID")
        self.run_count = int(os.getenv("RUN_COUNT"))
        self.run_time = os.getenv("RUN_TIME")
        self.min_stock_quantity = int(os.getenv("MIN_STOCK_QUANTITY"))


if __name__ == '__main__':
    settings = Settings()
    data_file_path = settings.data_file_path
    print(data_file_path)
