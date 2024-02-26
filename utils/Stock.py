import yfinance as yf
from finbert_utils import estimate_sentiment
from scrape_yahoo_news import grab_body_content
import concurrent.futures

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
        def process_links(link):
            content = grab_body_content(link)
            probability, sentiment = estimate_sentiment(content)
            return [probability, sentiment]
        

        news = self.stock.get_news()
        news_link = [new['link'] for new in news]

        data = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_links, link) for link in news_link]
            for future in futures:
                result = future.result()
                if result is not None:
                    data.append(result)

        return data
    
    def recommendation(self):
        data = self.get_sentiment_data()
        
        # Sort the data out
        results = {
            "positive": [],
            "neutral": [],
            "negative": []
        }

        for d in data:
            results[d[1]].append(d[0])

        averaged_results = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }

        for key in results.keys():
            average = 0
            for probability in results[key]:
                print(probability)
                average += probability
            
            divisor = len(results[key]) if len(results[key]) != 0 else 1
            average /= divisor
            averaged_results[key] = average
        
        return averaged_results
    
GOOGL = Stock("MSFT")
print(GOOGL.recommendation())