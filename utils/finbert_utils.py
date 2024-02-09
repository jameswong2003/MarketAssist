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
The S&P 500 is expected to face downward pressure on its valuation due to increased debt issuances by the U.S. Treasury.
The shift towards more long-term debt issuance will require higher interest rates, impacting the yield on 10-year T-notes.
The market is predicting 5 rate cuts, but the Federal Reserve is hinting at only 3, leading to potential increases in discount rates.
I think the ETF is a strong sell.
"""])
    print(tensor, sentiment)
    