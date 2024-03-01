from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 
from scrape_yahoo_news import grab_body_content
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


    