import pandas as pd
import numpy as np
import ta

class FeatureEngineer:
    def create(self, stock_data, news_data):
        features = {}
        for symbol, data in stock_data.items():
            if not data:
                continue
            df = pd.DataFrame(data)
            if 'close' in df.columns:
                df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
                df['sma'] = ta.trend.SMAIndicator(df['close']).sma_indicator()
                df['ema'] = ta.trend.EMAIndicator(df['close']).ema_indicator()
            features[symbol] = df.fillna(0).to_dict(orient='records')
        return features
