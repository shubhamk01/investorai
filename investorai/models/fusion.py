class FusionDecisionModel:
    def decide(self, price_preds, news_sents, features):
        actions = {}
        for symbol in price_preds:
            pred = price_preds[symbol]
            sent = news_sents.get(symbol, 0)
            if pred is None:
                actions[symbol] = "hold"
                continue
            # Simple fusion logic: buy if both positive, sell if both negative
            if pred > 0 and sent > 0.1:
                actions[symbol] = "buy"
            elif pred < 0 and sent < -0.1:
                actions[symbol] = "sell"
            else:
                actions[symbol] = "hold"
        return actions
