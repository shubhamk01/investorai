import torch
import torch.nn as nn
import numpy as np

class LSTMPriceModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, output_size=1):
        super(LSTMPriceModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        h0 = torch.zeros(self.lstm.num_layers, x.size(0), self.lstm.hidden_size)
        c0 = torch.zeros(self.lstm.num_layers, x.size(0), self.lstm.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class PricePredictor:
    def __init__(self, model_path="models/lstm_stock.pth", input_size=10):
        self.input_size = input_size
        self.model = LSTMPriceModel(input_size)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

    def predict(self, features):
        # features: dict of {symbol: np.array of shape (N, input_size)}
        preds = {}
        for symbol, X in features.items():
            X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
            with torch.no_grad():
                output = self.model(X_tensor)
                preds[symbol] = float(output.item())
        return preds