import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

def grab_body_content(news_link):
    request = requests.get(news_link, headers=headers)
    soup = BeautifulSoup(request.content, "html.parser")

    article_body = soup.find("div", class_="caas-body")
    try:
        article_text = article_body.find_all("p")
        content = ""
        for p in article_text:
            content += p.text
        
        return content
    except:
        raise Exception("No Yahoo Article found")

    