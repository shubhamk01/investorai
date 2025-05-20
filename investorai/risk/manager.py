class RiskManager:
    def __init__(self, risk_config, logger=None):
        self.max_position = risk_config.get("max_position", 0.1)
        self.stop_loss_pct = risk_config.get("stop_loss_pct", 0.02)
        self.logger = logger

    def get_position_size(self, symbol, capital, action):
        if self.logger:
            self.logger.info(f"Calculating position size for {symbol}, action: {action}")
        qty = int((capital * self.max_position) // 100)
        stop_loss = self.stop_loss_pct
        return qty, stop_loss
