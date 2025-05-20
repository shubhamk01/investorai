import time
from investorai.config.config import load_config
from investorai.adapters import BrokerAdapterFactory
from investorai.data_fetcher.alpha_vantage import AlphaVantageFetcher
from investorai.data_fetcher.news import NewsFetcher
from investorai.features.engineer import FeatureEngineer
from investorai.models.price_predictor import PricePredictor
from investorai.models.sentiment_analyzer import NewsSentimentAnalyzer
from investorai.models.fusion import FusionDecisionModel
from investorai.trader.engine import TradingEngine
from investorai.risk.manager import RiskManager
from investorai.logger.logger import Logger

def main():
    config = load_config()
    logger = Logger(config['log_path'])
    logger.info("Starting InvestorAI main loop.")

    try:
        # broker = BrokerAdapterFactory.create(config['broker'], config['api_keys'])  # Not used for stock data anymore
        stock_fetcher = AlphaVantageFetcher(api_key=config['alpha_vantage_api_key'], logger=logger)
        news_fetcher = NewsFetcher(config['news_api_keys'], logger=logger)
        feature_engineer = FeatureEngineer(logger=logger)
        price_predictor = PricePredictor(logger=logger)
        sentiment_analyzer = NewsSentimentAnalyzer(logger=logger)
        decision_model = FusionDecisionModel(logger=logger)
        risk_manager = RiskManager(config['risk'], logger=logger)
        trader = TradingEngine(None, risk_manager, logger=logger)  # Pass None for broker

        while True:
            logger.info("Fetching stock and news data.")
            stock_data = {}
            for symbol in config['stocks']:
                df = stock_fetcher.get_historical_data(
                    symbol,
                    start_date=config.get('start_date'),
                    end_date=config.get('end_date')
                )
                stock_data[symbol] = df.to_dict(orient='records') if not df.empty else []
            news_data = news_fetcher.fetch_all(config['stocks'])
            features = feature_engineer.create(stock_data, news_data)
            price_preds = price_predictor.predict(features)
            news_sents = sentiment_analyzer.analyze(news_data)
            actions = decision_model.decide(price_preds, news_sents, features)
            trader.execute(actions, config['capital'])
            logger.log(actions, price_preds, news_sents)
            print(actions, price_preds, news_sents)
            logger.info("Sleeping for interval: %s", config['run_interval'])
            time.sleep(config['run_interval'])
    except Exception as e:
        logger.error(f"Exception in main loop: {e}")
        raise

if __name__ == "__main__":
    main()