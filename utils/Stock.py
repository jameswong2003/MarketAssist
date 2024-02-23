import yfinance as yf
from finbert_utils import estimate_sentiment
from scrape_yahoo_news import grab_body_content

class Stock:
    def __init__(self, stock) -> None:
        self.stock = stock
        self.data = {}
        self.stock = yf.Ticker(stock)

        basic_info = self.get_basic_info()
        balance_sheet = self.get_balance_sheet()
        income_stmt = self.get_income_stmt()
        self.data.update(basic_info)
        self.data.update(balance_sheet)
        self.data.update(income_stmt)

    def get_basic_info(self):
        '''
        Scrape data from yahoo finance and store it as a dict
        '''
        basic_info = self.stock.info
        return basic_info
    
    def get_balance_sheet(self):
        balance_sheet = self.stock.get_balance_sheet()
        balance_sheet_dict = { 'balanceSheet': balance_sheet }
        return balance_sheet_dict
    
    def get_income_stmt(self):
        income_stmt = self.stock.get_income_stmt()
        income_stmt_dict = { 'incomeStatement': income_stmt }
        return income_stmt_dict

    def get_item(self, key):
        try:
            return self.data[key]
        except:
            return 'Not Available'
        
    def get_sentiment_data(self):
        news = self.stock.get_news()
        news_link = [new['link'] for new in news]

        data = []
        for link in news_link:
            try:
                content = grab_body_content(link)
                probability, sentiment = estimate_sentiment(content)
                data.append([probability, sentiment])
            except Exception as e:
                continue

        return data
    