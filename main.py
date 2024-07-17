# main.py
from datetime import datetime, timedelta
import time
from config import API_KEY, API_SECRET, BASE_URL
from trading_strategies import mean_reversion, momentum_trading
from order_manager import submit_order
from utils import get_profit_loss

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

def run_trading_bot():
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    initial_cash = float(api.get_account().cash)
    while True:
        now = datetime.now()
        if now.weekday() < 5:  # Check if it's a weekday
            start_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
            end_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

            if start_time <= now <= end_time:
                print("Trading session is active.")
                for symbol in nasdaq_100_symbols:
                    # Mean Reversion
                    mean_reversion_data = mean_reversion(symbol)
                    if mean_reversion_data['position'].iloc[-1] == 1:
                        submit_order(symbol, 100, 'buy')  # Invest $100 for each buy
                    elif mean_reversion_data['position'].iloc[-1] == -1:
                        submit_order(symbol, 100, 'sell')  # Sell equivalent amount
                    
                    # Momentum Trading
                    momentum_data = momentum_trading(symbol)
                    if momentum_data['position'].iloc[-1] == 1:
                        submit_order(symbol, 100, 'buy')  # Invest $100 for each buy
                    elif momentum_data['position'].iloc[-1] == -1:
                        submit_order(symbol, 100, 'sell')  # Sell equivalent amount
                
                current_cash = float(api.get_account().cash)
                profit_loss = get_profit_loss()
                print(f"Completed trading check for {len(nasdaq_100_symbols)} symbols.")
                print(f"Current Balance: ${current_cash:.2f}")
                print(f"Profit/Loss for the Day: ${profit_loss:.2f}")
                time.sleep(60)  # Run every minute
            else:
                message = "Outside trading hours. Sleeping until the next trading session."
                print(message)
                current_cash = float(api.get_account().cash)
                profit_loss = get_profit_loss()
                print(f"Current Balance: ${current_cash:.2f}")
                print(f"Profit/Loss for the Day: ${profit_loss:.2f}")
               
