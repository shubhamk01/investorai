import csv
import os
from datetime import datetime

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        if not os.path.exists(log_path):
            with open(log_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "symbol", "action", "price_pred", "sentiment"])

    def log(self, actions, price_preds, news_sents):
        with open(self.log_path, "a", newline="") as f:
            writer = csv.writer(f)
            ts = datetime.now().isoformat()
            for symbol, action in actions.items():
                writer.writerow([
                    ts, symbol, action, price_preds.get(symbol, ""), news_sents.get(symbol, "")
                ])
