# InvestorAI

**InvestorAI** is a modular, backend-only, AI-powered, broker-agnostic Indian stock market trading engine.

## Features

- Broker-agnostic adapters (Zerodha, Groww, Angel One)
- Modular data fetching for stocks and news
- Feature engineering with technical indicators
- LSTM-based price prediction (PyTorch)
- News sentiment analysis (FinBERT)
- Fusion model for trade decision
- Risk management (position sizing, stop-loss)
- Automated trading engine
- CSV logging of trades and predictions
- YAML-based configuration

## Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Configure `investorai/config/config.yaml` with your broker and API keys.
3. Run the main application:
   ```
   python main.py
   ```

## Disclaimer

This project is for educational and research purposes only. Trading in financial markets involves significant risk. The authors are not responsible for any financial losses incurred. Use at your own risk.
