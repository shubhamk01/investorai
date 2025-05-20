class TradingEngine:
    def __init__(self, broker_adapter, risk_manager):
        self.broker = broker_adapter
        self.risk_manager = risk_manager

    def execute(self, actions, capital):
        for symbol, action in actions.items():
            if action == "hold":
                continue
            qty, stop_loss = self.risk_manager.get_position_size(symbol, capital, action)
            if qty <= 0:
                continue
            price = self.broker.fetch_realtime_quote(symbol).get("price", None)
            if price is None:
                continue
            self.broker.place_order(symbol, qty, action, "market", price)
