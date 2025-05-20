def make_decision(stock, trend, sentiment, capital):
    if trend == 'uptrend' and sentiment == 'positive':
        return {'action': 'buy', 'amount': capital * 0.3}
    elif trend == 'downtrend' and sentiment == 'negative':
        return {'action': 'sell', 'amount': 0}
    else:
        return {'action': 'hold', 'amount': 0}
