from abc import ABC, abstractmethod

class BaseBrokerAdapter(ABC):
    @abstractmethod
    def authenticate(self, api_keys: dict):
        pass

    @abstractmethod
    def fetch_historical_data(self, symbol: str, start_date: str, end_date: str, interval: str):
        pass

    @abstractmethod
    def fetch_realtime_quote(self, symbol: str):
        pass

    @abstractmethod
    def place_order(self, symbol: str, qty: int, side: str, order_type: str, price: float = None):
        pass

    @abstractmethod
    def get_portfolio(self):
        pass
