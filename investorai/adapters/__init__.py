from .zerodha import ZerodhaAdapter
from .groww import GrowwAdapter
from .angel import AngelAdapter

class BrokerAdapterFactory:
    @staticmethod
    def create(broker_name: str, api_keys: dict, logger=None):
        broker_name = broker_name.lower()
        if broker_name == "zerodha":
            return ZerodhaAdapter(api_keys, logger)
        elif broker_name == "groww":
            return GrowwAdapter(api_keys, logger)
        elif broker_name == "angel":
            return AngelAdapter(api_keys, logger)
        else:
            if logger:
                logger.error(f"Unsupported broker: {broker_name}")
            raise ValueError(f"Unsupported broker: {broker_name}")

__all__ = ["BrokerAdapterFactory"]
