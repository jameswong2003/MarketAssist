from utils.Stock import Stock

stock = input('Stock that you would like to look at\n')

stock = Stock(stock)
print(stock.data)

while True:
    option = input('What part of the stock would you like to look at')
    print(stock.get_item(key=option))