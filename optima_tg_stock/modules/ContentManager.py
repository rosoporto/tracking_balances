from .custom_logging import Logger
from .DataModule import DataModule
from ..config.settings import Settings


class ContentManager:
    def __init__(self, data_file_path, min_stock_quantity, logger):
        self.data_module = DataModule(data_file_path, logger)
        self.min_stock_quantity = min_stock_quantity
        self.logger = logger

    def get_data(self):
        """
        Returns:
            json: Returns product details in the form product: balance
        """
        return self.data_module.process_data()

    def create_answer(self, flag='alert'):
        massages = self.get_data()
        if not massages:
            self.logger.error("Данные отсутствуют")
            raise ValueError("Значение не может быть пустым")
        else:
            massages = {key: int(value) for key, value in massages.items()}
            result = []
            for product, stock in massages.items():
                stock_product = ''
                if stock == 0:
                    stock_product = f'{product} закончился'
                elif self.check_stock(self.min_stock_quantity, stock):                    
                    stock_product = f'{product}: осталось *{stock}* шт.'
                elif flag != 'alert':
                    stock_product = f'{product}: {stock} шт.'
                else:
                    continue
                result.append(stock_product)
            if any(result):
                return '\n'.join(result)
            else:
                return None

    def check_stock(self, min_stock_quantity, stock):
        if stock:
            return True if min_stock_quantity >= stock else False
        else:
            return False


def main():
    settings = Settings()
    logger = Logger(settings.path_to_log)

    content_manager = ContentManager(
        settings.data_file_path,
        settings.min_stock_quantity,
        logger
    )
    print(content_manager.create_answer())


if __name__ == '__main__':
    main()
