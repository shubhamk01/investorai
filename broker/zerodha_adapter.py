class Zerodha:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        # Simulate login
        print(f"Logged into Zerodha with API Key: {api_key}")

    def place_order(self, stock, action, quantity):
        print(f"[Zerodha] {action.upper()} {quantity} shares of {stock}")
