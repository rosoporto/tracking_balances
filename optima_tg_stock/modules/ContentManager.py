from .custom_logging import Logger


class ContentManager:
    def __init__(self, massages, min_stock_quantity, logger):
        self.massages = massages
        self.min_stock_quantity = min_stock_quantity
        self.logger = logger

    def create_answer(self):
        if not self.massages:
            self.logger.error("Данные отсутствуют")
            raise ValueError("Значение не может быть пустым")
        else:
            result = []
            for product, stock in self.massages.items():
                stock_product = ''
                if self.check_stock(self, self.min_stock_quantity, stock):
                    stock_product = f'\033[31mВНИМАНИЕ!\033[0m {product}: осталось *{stock}* шт.'
                else:
                    stock_product = f'{product}: {stock} шт.'
                result.append(stock_product)
        return '\n'.join(result)

    def check_stock(self, min_stock_quantity, stock):
        if stock:
            return True if min_stock_quantity >= stock else False
        else:
            return False
