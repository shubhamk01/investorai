import requests
import pandas as pd
from datetime import datetime
from typing import Optional

class AlphaVantageFetcher:
    """
    Fetches stock data from Alpha Vantage API for both Indian and foreign stocks.

    Args:
        api_key (str): Alpha Vantage API key.
        logger (optional): Logger instance for logging info and errors.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str, logger=None):
        self.api_key = api_key
        self.logger = logger
        if self.logger:
            self.logger.info("AlphaVantageFetcher initialized.")

    def get_historical_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch historical daily data for a given symbol.

        Args:
            symbol (str): Stock symbol (e.g., "RELIANCE.NSE", "AAPL").
            start_date (str, optional): Start date in "YYYY-MM-DD".
            end_date (str, optional): End date in "YYYY-MM-DD".

        Returns:
            pd.DataFrame: DataFrame with historical OHLCV data.
        """
        if self.logger:
            self.logger.info(f"AlphaVantage: Fetching historical data for {symbol} from {start_date} to {end_date}")
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "full"
        }
        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=30)
            if self.logger:
                self.logger.info(f"AlphaVantage: HTTP GET {resp.url} status {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            # Enhanced error logging for Alpha Vantage API
            if "Time Series (Daily)" not in data:
                # Log the full response for debugging
                if self.logger:
                    self.logger.error(f"AlphaVantage error for {symbol}: {data}")
                msg = data.get("Note") or data.get("Error Message") or "Unknown error"
                if self.logger:
                    self.logger.error(f"AlphaVantage error for {symbol}: {msg}")
                return pd.DataFrame()
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index", dtype=float)
            df.index = pd.to_datetime(df.index)
            df = df.rename(columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. adjusted close": "adj_close",
                "6. volume": "volume",
                "7. dividend amount": "dividend",
                "8. split coefficient": "split_coef"
            })
            if start_date:
                df = df[df.index >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df.index <= pd.to_datetime(end_date)]
            df = df.sort_index()
            if self.logger:
                self.logger.info(f"AlphaVantage: Retrieved {len(df)} rows for {symbol}")
            return df
        except Exception as e:
            if self.logger:
                self.logger.error(f"AlphaVantage exception for {symbol}: {e}")
            return pd.DataFrame()

    def get_current_price(self, symbol: str) -> pd.DataFrame:
        """
        Fetch the latest price/current data for a given symbol.

        Args:
            symbol (str): Stock symbol (e.g., "RELIANCE.NSE", "AAPL").

        Returns:
            pd.DataFrame: DataFrame with the latest price and timestamp.
        """
        if self.logger:
            self.logger.info(f"AlphaVantage: Fetching current price for {symbol}")
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=30)
            if self.logger:
                self.logger.info(f"AlphaVantage: HTTP GET {resp.url} status {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            if "Global Quote" not in data or not data["Global Quote"]:
                msg = data.get("Note") or data.get("Error Message") or "Unknown error"
                if self.logger:
                    self.logger.error(f"AlphaVantage error for {symbol}: {msg}")
                return pd.DataFrame()
            quote = data["Global Quote"]
            df = pd.DataFrame([{
                "symbol": quote.get("01. symbol"),
                "open": float(quote.get("02. open", 0)),
                "high": float(quote.get("03. high", 0)),
                "low": float(quote.get("04. low", 0)),
                "price": float(quote.get("05. price", 0)),
                "volume": float(quote.get("06. volume", 0)),
                "latest_trading_day": quote.get("07. latest trading day"),
                "previous_close": float(quote.get("08. previous close", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": quote.get("10. change percent")
            }])
            if self.logger:
                self.logger.info(f"AlphaVantage: Current price for {symbol} is {df.at[0, 'price'] if not df.empty else 'N/A'}")
            return df
        except Exception as e:
            if self.logger:
                self.logger.error(f"AlphaVantage exception for {symbol}: {e}")
            return pd.DataFrame()
