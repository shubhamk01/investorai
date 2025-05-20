from .zerodha import ZerodhaAdapter
from .groww import GrowwAdapter
from .angel import AngelAdapter

__all__ = ["BrokerAdapterFactory"]

class BrokerAdapterFactory:
    @staticmethod
    def create(broker_name: str, api_keys: dict):
        broker_name = broker_name.lower()
        if broker_name == "zerodha":
            return ZerodhaAdapter(api_keys)
        elif broker_name == "groww":
            return GrowwAdapter(api_keys)
        elif broker_name == "angel":
            return AngelAdapter(api_keys)
        else:
            raise ValueError(f"Unsupported broker: {broker_name}")
