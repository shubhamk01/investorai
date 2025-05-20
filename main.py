import time
from config.config import load_config
from adapters import BrokerAdapterFactory
from data_fetcher.stock import StockDataFetcher
from data_fetcher.news import NewsFetcher
from features.engineer import FeatureEngineer
from models.price_predictor import PricePredictor
from models.sentiment_analyzer import NewsSentimentAnalyzer
from models.fusion import FusionDecisionModel
from trader.engine import TradingEngine
from risk.manager import RiskManager
from logger.logger import Logger

def main():
    config = load_config()

    broker = BrokerAdapterFactory.create(config['broker'], config['api_keys'])
    stock_fetcher = StockDataFetcher(broker)
    news_fetcher = NewsFetcher(config['news_api_keys'])
    feature_engineer = FeatureEngineer()
    price_predictor = PricePredictor()
    sentiment_analyzer = NewsSentimentAnalyzer()
    decision_model = FusionDecisionModel()
    risk_manager = RiskManager(config['risk'])
    trader = TradingEngine(broker, risk_manager)
    logger = Logger(config['log_path'])

    while True:
        stock_data = stock_fetcher.fetch_all(config['stocks'])
        news_data = news_fetcher.fetch_all(config['stocks'])
        features = feature_engineer.create(stock_data, news_data)
        price_preds = price_predictor.predict(features)
        news_sents = sentiment_analyzer.analyze(news_data)
        actions = decision_model.decide(price_preds, news_sents, features)
        trader.execute(actions, config['capital'])
        logger.log(actions, price_preds, news_sents)
        time.sleep(config['run_interval'])

if __name__ == "__main__":
    main()