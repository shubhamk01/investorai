class StockDataFetcher:
    def __init__(self, broker_adapter):
        self.broker = broker_adapter

    def fetch_all(self, symbols, start_date=None, end_date=None, interval="1d"):
        data = {}
        for symbol in symbols:
            data[symbol] = self.broker.fetch_historical_data(
                symbol, start_date, end_date, interval
            )
        return data
