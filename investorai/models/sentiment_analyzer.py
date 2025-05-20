from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class NewsSentimentAnalyzer:
    def __init__(self, logger=None, model_name="ProsusAI/finbert"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.logger = logger

    def analyze(self, news_data):
        if self.logger:
            self.logger.info("Analyzing news sentiment.")
        sentiments = {}
        for symbol, articles in news_data.items():
            scores = []
            for article in articles:
                try:
                    text = article.get("headline", "") + " " + article.get("content", "")
                    inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
                    with torch.no_grad():
                        outputs = self.model(**inputs)
                        probs = torch.softmax(outputs.logits, dim=1).numpy()[0]
                        score = probs[2] - probs[0]
                        scores.append(score)
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Error analyzing sentiment for {symbol}: {e}")
            sentiments[symbol] = float(np.mean(scores)) if scores else 0.0
        return sentiments
