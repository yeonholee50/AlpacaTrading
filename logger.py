# logger.py
import logging
from datetime import datetime

logging.basicConfig(filename='trading_bot.log', level=logging.INFO)

def log_trade(symbol, side, qty, price):
    message = f"{datetime.now()} - {side} {qty} shares of {symbol} at ${price}"
    logging.info(message)
    print(message)
