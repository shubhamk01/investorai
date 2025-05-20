class RiskManager:
    def __init__(self, risk_config):
        self.max_position = risk_config.get("max_position", 0.1)
        self.stop_loss_pct = risk_config.get("stop_loss_pct", 0.02)

    def get_position_size(self, symbol, capital, action):
        # Simple fixed-fractional position sizing
        qty = int((capital * self.max_position) // 100)  # Placeholder: 100 = price
        stop_loss = self.stop_loss_pct
        return qty, stop_loss
