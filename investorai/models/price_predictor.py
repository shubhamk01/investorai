import torch
import torch.nn as nn
import numpy as np

class LSTMPricePredictor(nn.Module):
    def __init__(self, input_size=5, hidden_size=32, num_layers=2, output_size=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

class PricePredictor:
    def __init__(self, logger=None):
        self.model = LSTMPricePredictor()
        self.logger = logger
        # Placeholder: load model weights if available

    def predict(self, features):
        if self.logger:
            self.logger.info("Predicting prices using LSTM model.")
        preds = {}
        for symbol, feats in features.items():
            if not feats:
                preds[symbol] = None
                continue
            try:
                arr = np.array([[f.get('close', 0), f.get('rsi', 0), f.get('sma', 0), f.get('ema', 0), 0] for f in feats])
                arr = torch.tensor(arr, dtype=torch.float32).unsqueeze(0)
                with torch.no_grad():
                    pred = self.model(arr).item()
                preds[symbol] = pred
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error predicting price for {symbol}: {e}")
                preds[symbol] = None
        return preds
