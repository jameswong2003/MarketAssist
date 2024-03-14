from utils.Stock import Stock
import pandas as pd

csv = pd.read_csv("fortune500.csv")
print(csv)

tickers = csv["symbol"].tolist()
print(tickers)

for ticker in tickers:
    t = Stock(ticker)
    suggestion = t.recommendation()

    if suggestion == "positive":
        print(ticker)