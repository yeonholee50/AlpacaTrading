# order_manager.py
import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL
from logger import log_trade

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def submit_order(symbol, cash_amount, side):
    try:
        price = api.get_last_trade(symbol).price
        qty = cash_amount / price

        if side == 'buy':
            available_cash = float(api.get_account().cash)
            if cash_amount > available_cash:
                message = f"Insufficient funds to {side} {qty} shares of {symbol} at ${price}. Available cash: ${available_cash}"
                log_trade(symbol, side, 0, 0)
                print(message)
                return
        
        order = api.submit_order(
            symbol=symbol, 
            qty=qty, 
            side=side, 
            type='market', 
            time_in_force='day'
        )
        log_trade(symbol, side, qty, price)
    except Exception as e:
        log_trade(symbol, side, 0, 0)
        print(f"Error submitting order for {symbol}: {e}")
