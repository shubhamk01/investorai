from abc import ABC, abstractmethod

class BaseBrokerAdapter(ABC):
    def __init__(self, logger=None):
        self.logger = logger

    @abstractmethod
    def authenticate(self, api_keys: dict):
        if self.logger:
            self.logger.info("Authenticating with broker adapter.")
        pass

    @abstractmethod
    def fetch_historical_data(self, symbol: str, start_date: str, end_date: str, interval: str):
        if self.logger:
            self.logger.info(f"Fetching historical data for {symbol}.")
        pass

    @abstractmethod
    def fetch_realtime_quote(self, symbol: str):
        if self.logger:
            self.logger.info(f"Fetching real-time quote for {symbol}.")
        pass

    @abstractmethod
    def place_order(self, symbol: str, qty: int, side: str, order_type: str, price: float = None):
        if self.logger:
            self.logger.info(f"Placing order: {side} {qty} {symbol} at {price}.")
        pass

    @abstractmethod
    def get_portfolio(self):
        if self.logger:
            self.logger.info("Fetching portfolio.")
        pass
