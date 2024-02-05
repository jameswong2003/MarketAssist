from Stock import Stock

class Portfolio:
    def __init__(self):
        self.stock_holdings = {} # SYMBOL : # of shares
        self.value_history = {}

    def add_to_portfolio(self, stock: str, value: int):
        stock = Stock(stock)
        self.stock_holdings = self.stock_holdings.get(stock, 0) + value

    def get_current_value(self):
        current_value = 0
        for key in self.stock_holdings.keys():
            stock = Stock(key)
            stock_value = stock.get_item("currentPrice")
            current_value += stock_value
        
        return current_value
    
