import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging

# API keys
API_KEY = 'PKCTIXCLD4JLZ64F5B9S'
API_SECRET = 'BaNlmKqrpSpXxqEd7qbzPsbs4tAkyMu5bBXfVgP8'
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
account = api.get_account()

# List of NASDAQ 100 symbols
nasdaq_100_symbols = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'PYPL', 'ADBE', 'CMCSA',
    'NFLX', 'PEP', 'INTC', 'CSCO', 'AVGO', 'TXN', 'QCOM', 'COST', 'SBUX', 'AMD',
    'AMGN', 'CHTR', 'ISRG', 'INTU', 'MDLZ', 'MU', 'AMAT', 'BKNG', 'ADI', 'LRCX',
    'ASML', 'ADP', 'GILD', 'FISV', 'VRTX', 'CSX', 'MELI', 'ATVI', 'BIIB', 'KLAC',
    'MAR', 'XEL', 'KHC', 'SNPS', 'LULU', 'ORLY', 'MCHP', 'MNST', 'IDXX', 'CDNS',
    'CTAS', 'EBAY', 'ADSK', 'WDAY', 'ROST', 'TEAM', 'VRSK', 'CTSH', 'ALGN', 'ANSS',
    'DXCM', 'REGN', 'WBA', 'SGEN', 'SWKS', 'SPLK', 'VRSN', 'INCY', 'CHKP', 'EXC',
    'NTES', 'FAST', 'ILMN', 'BIDU', 'ZS', 'PCAR', 'CPRT', 'NXPI', 'PAYX', 'EA',
    'CERN', 'CDW', 'TTWO', 'OKTA', 'LBTYA', 'BMRN', 'ULTA', 'WDC', 'CTXS', 'JBHT',
    'DLTR', 'AEP', 'FOX', 'FOXA', 'SIRI', 'DISCA', 'DISCK'
]

# Logging setup
logging.basicConfig(filename='trading_bot.log', level=logging.INFO)

def log_trade(symbol, side, qty, price):
    logging.info(f"{datetime.now()} - {side} {qty} shares of {symbol} at ${price}")

def submit_order(symbol, qty, side):
    try:
        order = api.submit_order(symbol=symbol, qty=qty, side=side, type='market', time_in_force='day')
        log_trade(symbol, side, qty, order.filled_avg_price)
    except Exception as e:
        logging.error(f"Error submitting order for {symbol}: {e}")

def mean_reversion(symbol, short_window=40, long_window=100):
    data = api.get_barset(symbol, 'minute', limit=long_window).df[symbol]
    data['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1).mean()
    data['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1).mean()
    data['signal'] = 0
    data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1, 0)
    data['position'] = data['signal'].diff()
    return data

def momentum_trading(symbol, window=14):
    data = api.get_barset(symbol, 'minute', limit=window).df[symbol]
    data['momentum'] = data['close'] / data['close'].shift(window) - 1
    data['signal'] = np.where(data['momentum'] > 0, 1, 0)
    data['position'] = data['signal'].diff()
    return data

def arbitrage(symbol1, symbol2):
    data1 = api.get_barset(symbol1, 'minute', limit=100).df[symbol1]
    data2 = api.get_barset(symbol2, 'minute', limit=100).df[symbol2]
    spread = data1['close'] - data2['close']
    zscore = (spread - spread.mean()) / spread.std()
    data1['position'] = np.where(zscore > 1, -1, np.where(zscore < -1, 1, 0))
    data2['position'] = -data1['position']
    return data1, data2

def run_trading_bot():
    start_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)

    while datetime.now() < start_time:
        time.sleep(1)

    while datetime.now() < end_time:
        for symbol in nasdaq_100_symbols:
            # Mean Reversion
            mean_reversion_data = mean_reversion(symbol)
            if mean_reversion_data['position'].iloc[-1] == 1:
                submit_order(symbol, 1, 'buy')
            elif mean_reversion_data['position'].iloc[-1] == -1:
                submit_order(symbol, 1, 'sell')
            
            # Momentum Trading
            momentum_data = momentum_trading(symbol)
            if momentum_data['position'].iloc[-1] == 1:
                submit_order(symbol, 1, 'buy')
            elif momentum_data['position'].iloc[-1] == -1:
                submit_order(symbol, 1, 'sell')
        
        time.sleep(60)  # Run every minute

    logging.info("Trading session ended.")

if __name__ == "__main__":
    run_trading_bot()
