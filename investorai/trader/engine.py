class TradingEngine:
    def __init__(self, broker_adapter, risk_manager, logger=None):
        self.broker = broker_adapter
        self.risk_manager = risk_manager
        self.logger = logger

    def execute(self, actions, capital):
        if self.logger:
            self.logger.info("Executing trades.")
        for symbol, action in actions.items():
            if action == "hold":
                continue
            try:
                qty, stop_loss = self.risk_manager.get_position_size(symbol, capital, action)
                if qty <= 0:
                    continue
                price = self.broker.fetch_realtime_quote(symbol).get("price", None)
                if price is None:
                    continue
                self.broker.place_order(symbol, qty, action, "market", price)
                if self.logger:
                    self.logger.info(f"Executed {action} order for {symbol}, qty: {qty}, price: {price}")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error executing trade for {symbol}: {e}")
