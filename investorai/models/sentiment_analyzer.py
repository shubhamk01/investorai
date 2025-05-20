from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class NewsSentimentAnalyzer:
    def __init__(self, model_name="ProsusAI/finbert"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def analyze(self, news_data):
        sentiments = {}
        for symbol, articles in news_data.items():
            scores = []
            for article in articles:
                text = article.get("headline", "") + " " + article.get("content", "")
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    probs = torch.softmax(outputs.logits, dim=1).numpy()[0]
                    # FinBERT: [negative, neutral, positive]
                    score = probs[2] - probs[0]
                    scores.append(score)
            sentiments[symbol] = float(np.mean(scores)) if scores else 0.0
        return sentiments
