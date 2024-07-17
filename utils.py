# utils.py
import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def get_profit_loss():
    positions = api.list_positions()
    total_pl = 0.0
    for position in positions:
        total_pl += float(position.unrealized_pl)
    return total_pl
