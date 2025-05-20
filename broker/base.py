class BrokerAdapterBase:
    def authenticate(self):
        raise NotImplementedError

    def fetch_historical_data(self, symbol, start, end):
        raise NotImplementedError

    def fetch_realtime_quote(self, symbol):
        raise NotImplementedError

    def place_order(self, symbol, action, quantity):
        raise NotImplementedError

    def get_portfolio(self):
        raise NotImplementedError