import pandas as pd

# You can use NSE India's official API via nsepython (recommended for Indian stocks)
# Install: pip install nsepython
from nsepython import nsefetch

def get_stock_data(stock_symbol):
    """
    Fetch historical stock data for Indian stocks using NSE's API.
    Returns a pandas DataFrame with OHLCV data for the last 6 months.
    """
    # NSE symbol format: RELIANCE, TCS, INFY, etc. (no .NS)
    url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={stock_symbol}&series=[%22EQ%22]&from=2023-11-20&to=2024-05-20"
    # You may need to update the date range dynamically
    data = nsefetch(url)
    if "data" in data:
        df = pd.DataFrame(data["data"])
        # Convert date and numeric columns
        df['CH_TIMESTAMP'] = pd.to_datetime(df['CH_TIMESTAMP'])
        for col in ['CH_OPENING_PRICE', 'CH_CLOSING_PRICE', 'CH_TRADE_HIGH_PRICE', 'CH_TRADE_LOW_PRICE', 'CH_TOT_TRADED_QTY']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.rename(columns={
            'CH_TIMESTAMP': 'Date',
            'CH_OPENING_PRICE': 'Open',
            'CH_CLOSING_PRICE': 'Close',
            'CH_TRADE_HIGH_PRICE': 'High',
            'CH_TRADE_LOW_PRICE': 'Low',
            'CH_TOT_TRADED_QTY': 'Volume'
        })
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df = df.sort_values('Date')
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data

# Best resource for Indian stock data: 
# - [nsepython](https://github.com/1fin/nsepython) (official NSE API wrapper, reliable for Indian stocks)
# - [NSE official website](https://www.nseindia.com/)
