# trading_strategies.py
import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
from config import API_KEY, API_SECRET, BASE_URL

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

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
