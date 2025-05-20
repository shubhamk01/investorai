from broker.zerodha_adapter import Zerodha
from data.stock_data_fetcher import get_stock_data
from data.news_aggregator import get_news
from model.lstm_predictor import predict_trend
from model.sentiment_analyzer import analyze_sentiment
from engine.decision_engine import make_decision
from engine.trade_executor import execute_trade

capital = 100000  # User input
broker = Zerodha(api_key="your_api_key", api_secret="your_api_secret")

stocks = ['TCS', 'INFY', 'RELIANCE']
for stock in stocks:
    df = get_stock_data(stock)
    news = get_news(stock)
    trend = predict_trend(df)
    sentiment = analyze_sentiment(news)
    decision = make_decision(stock, trend, sentiment, capital)
    execute_trade(broker, stock, decision)
