import pandas as pd
import numpy as np
import ta

class FeatureEngineer:
    def __init__(self, logger=None):
        self.logger = logger

    def create(self, stock_data, news_data):
        if self.logger:
            self.logger.info("Engineering features from stock and news data.")
        features = {}
        for symbol, data in stock_data.items():
            if not data:
                continue
            try:
                df = pd.DataFrame(data)
                if 'close' in df.columns:
                    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
                    df['sma'] = ta.trend.SMAIndicator(df['close']).sma_indicator()
                    df['ema'] = ta.trend.EMAIndicator(df['close']).ema_indicator()
                features[symbol] = df.fillna(0).to_dict(orient='records')
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error engineering features for {symbol}: {e}")
                features[symbol] = []
        return features
