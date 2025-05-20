class StockDataFetcher:
    def __init__(self, broker_adapter, logger=None):
        self.broker = broker_adapter
        self.logger = logger

    def fetch_all(self, symbols, start_date=None, end_date=None, interval="1d"):
        if self.logger:
            self.logger.info(f"Fetching stock data for symbols: {symbols}")
        data = {}
        for symbol in symbols:
            try:
                data[symbol] = self.broker.fetch_historical_data(
                    symbol, start_date, end_date, interval
                )
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error fetching data for {symbol}: {e}")
                data[symbol] = []
        return data
