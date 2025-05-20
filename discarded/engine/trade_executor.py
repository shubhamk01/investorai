def execute_trade(broker, stock, decision):
    """
    Executes a trade decision using the broker's API.
    decision: dict with keys 'action' (buy/sell/hold), 'amount' (float)
    """
    action = decision['action']
    amount = decision.get('amount', 0)
    price_per_share = broker.get_current_price(stock)  # Use broker's price fetch
    quantity = int(amount / price_per_share) if price_per_share > 0 else 0

    if action == 'buy' and quantity > 0:
        broker.place_order(stock, action, quantity)
        print(f"BUY {quantity} shares of {stock} at {price_per_share}")
    elif action == 'sell':
        # Sell all holdings or a specified quantity
        holdings = broker.get_holdings(stock)
        sell_qty = min(holdings, quantity) if quantity > 0 else holdings
        if sell_qty > 0:
            broker.place_order(stock, action, sell_qty)
            print(f"SELL {sell_qty} shares of {stock} at {price_per_share}")
        else:
            print(f"No holdings to sell for {stock}")
    else:
        print(f"HOLDING {stock}")
