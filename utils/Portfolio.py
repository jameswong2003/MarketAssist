from Stock import Stock

class Portfolio:
    def __init__(self):
        self.stock_holdings = {} # SYMBOL : # of shares
        self.value_history = {}

    def add_to_portfolio(self, stock: str, value: int):
        stock = Stock(stock)
        self.stock_holdings = self.stock_holdings.get(stock, 0) + value

    def update_value_history(self):
        current_value = 0
        for key in self.stock_holdings.keys():
            stock = Stock(stock)
            stock_value = stock.get_item()