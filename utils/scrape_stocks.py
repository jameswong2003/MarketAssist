import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

request = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').text
soup = BeautifulSoup(request, 'html.parser')

table = soup.find(id='constituents')

df = pd.DataFrame(columns=['symbol', 'security'])
for row in table.find_all('tr'):
    columns = row.find_all('td')

    if (columns != []):
        symbol = columns[0].text.strip()
        company_name = columns[1].text.strip()
        df = df._append({'symbol': symbol, 'security': company_name}, ignore_index=True)

file_name = "./fortune500.csv"

df.to_csv(file_name, encoding='utf-8', index=False)