from .zerodha import ZerodhaAdapter
from .groww import GrowwAdapter
from .angel import AngelAdapter

class BrokerAdapterFactory:
    @staticmethod
    def create(broker, api_keys):
        if broker == "zerodha":
            return ZerodhaAdapter(api_keys)
        elif broker == "groww":
            return GrowwAdapter(api_keys)
        elif broker == "angel":
            return AngelAdapter(api_keys)
        else:
            raise ValueError("Unsupported broker")