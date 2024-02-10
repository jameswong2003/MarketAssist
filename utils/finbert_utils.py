from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 
device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news):
    if news:
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]


if __name__ == "__main__":
    tensor, sentiment = estimate_sentiment(["""
A lot can change on the stock market in just a few years, and Pfizer (NYSE: PFE) is a great example. At the end of 2021, its shares were trading at around $60, and things were looking great for the COVID-19 vaccine maker. It would go on to hit a record of more than $100 billion in annual revenue in 2022.Today, however, the stock is below $30 per share. What was once hype and excitement surrounding the stock has now been replaced with fear and concern as investors worry about what the future holds for the business.Revenue from its COVID-19 products likely won't ever be as strong as it was in 2022. But the problems for Pfizer go even deeper. Here's why.On Jan. 30, Pfizer posted its quarterly results for the last three months of 2023, and they weren't great. Revenue was down to just $14.2 billion, declining by more than 41% year over year. And the company also incurred a $3.4 billion net loss, largely due to a revenue reversal involving Paxlovid, its COVID pill.While many investors likely know about Pfizer's struggles with its COVID products, the company isn't just struggling on that front. Its oncology business experienced a 3% decline last quarter, and specialty care sales were only up by 11%.Here's a breakdown of the company's non-COVID products which generated more than $1 billion in revenue last quarter:ProductRevenueYear-Over-Year ChangeEliquis$1.6 billion9%Prevnar$1.6 billion-8%Ibrance$1.1 billion-13%Data source: Company filings.Anticoagulant medication Eliquis was the only product with more than $1 billion in sales and generated positive year-over-year growth. The company's Vyndaqel brand (which helps treat transthyretin amyloidosis, a protein disorder) came close, with revenue of $961 million growing by 41%, but generally, the results haven't been strong from Pfizer's top products.What's concerning is that even with its recent $43 billion acquisition of oncology company Seagen, Pfizer is only projecting revenue to total between $58.5 billion to $61.5 billion for this year, which would be little or no growth from the $58.5 billion it reported for 2023.Pfizer is facing a tough road ahead as it faces patent cliffs and rising competition. And while acquisitions will bolster its pipeline and give it some hope that there could be help for the top line in the future, it's still an uncertain path, which investors haven't been eager to join the company on. In the past 12 months, the healthcare stock has fallen by 39%.Pfizer is a company in transition, and it may take multiple years before the company gets back to generating growth. But if you're willing to take a chance on the company, it could prove to be one of the better investments in the long run as Pfizer's stock is deeply discounted, trading at levels it hasn't seen since 2014. There is some risk with the stock, but there can also be tremendous upside for investors who are patient.Should you invest $1,000 in Pfizer right now?Before you buy stock in Pfizer, consider this:The Motley Fool Stock Advisor analyst team just identified what they believe are the 10 best stocks for investors to buy now… and Pfizer wasn’t one of them. The 10 stocks that made the cut could produce monster returns in the coming years.Stock Advisor provides investors with an easy-to-follow blueprint for success, including guidance on building a portfolio, regular updates from analysts, and two new stock picks each month. The Stock Advisor service has more than tripled the return of S&P 500 since 2002*.See the 10 stocks*Stock Advisor returns as of February 5, 2024David Jagielski has no position in any of the stocks mentioned. The Motley Fool has positions in and recommends Pfizer. The Motley Fool has a disclosure policy.Pfizer's Problems Go Far Beyond Just Declining COVID Revenue was originally published by The Motley Fool≈
"""])
    print(tensor, sentiment)
    