
order_usd_size = 10

leverage = 3 
timeframe = '4h'

# Define symbol-specific parameters
symbols = ['WIF', 'POPCAT']
symbols_data = {
    'WIF': {
        'sma_period': 14,
        'buy_range': (14, 15),
        'sell_range': (14, 22)
    },
    'POPCAT': {
        'sma_period': 14,
        'buy_range': (12, 13),
        'sell_range': (14, 18)
    }
}


# Function to get the buy/sell range for a symbol
def get_ranges(symbol):
    return symbols_data.get(symbol, {'buy_range': (0, 0), 'sell_range': (0, 0)})

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
import nice_funcs as n 
from eth_account.signers.local import LocalAccount
import eth_account
import json
import time, random  
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import ccxt
import pandas as pd
import schedule
import requests

# Import secret key from credentials folder
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from credentials.api_secrets import HYPERLIQUID_SECRET_KEY as secret

# Fetch symbols from the API
def get_symbols():
    url = 'https://api.hyperliquid.xyz/info'
    headers = {'Content-Type': 'application/json'}
    data = {'type': 'meta'}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print('Error:', response.status_code)
        return []

    data = response.json()
    symbols = [symbol['name'] for symbol in data['universe']]
    print("Fetched Symbols:", symbols)
    return symbols

# Fetch candle snapshot for a given symbol and time range
def fetch_candle_snapshot(symbol, interval, start_time, end_time):
    url = 'https://api.hyperliquid.xyz/info'
    headers = {'Content-Type': 'application/json'}
    data = {
        "type": "candleSnapshot",
        "req": {
            "coin": symbol,
            "interval": interval,
            "startTime": int(start_time.timestamp() * 1000),
            "endTime": int(end_time.timestamp() * 1000)
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        snapshot_data = response.json()
        if 'candles' in snapshot_data:
            return snapshot_data['candles']
        else:
            return snapshot_data  # Adjust if the structure is different
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None

# Fetch daily data for calculating resistance levels
def fetch_daily_data(symbol, days=20):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    return fetch_candle_snapshot(symbol, '1d', start_time, end_time)

# Calculate daily resistance levels
def calculate_daily_resistance(symbols):
    resistance_levels = {}
    for symbol in symbols:
        daily_data = fetch_daily_data(symbol)
        if daily_data:
            high_prices = [float(day['h']) for day in daily_data]
            resistance_levels[symbol] = max(high_prices)
            print(f"Resistance level for {symbol}: {resistance_levels[symbol]}")
    return resistance_levels


# Calculate the breakout strategy conditions
def check_breakout(symbol, hourly_snapshots, daily_resistance):
    #print(hourly_snapshots)
    current_close = float(hourly_snapshots['close'].iloc[-1])
    print(f'current close {current_close}')

    # Get the daily resistance level
    daily_resistance_level = daily_resistance.get(symbol, None)
    print(f'this is the daily resistance {daily_resistance_level}')
    if not daily_resistance_level:
        print(f"Daily resistance level not found for {symbol}")
        return None

    print(f'current close: {current_close} resistance level: {daily_resistance_level}')
 # TODO - change back to >   
    if current_close > daily_resistance_level:
        entry_price = current_close
        stop_loss = entry_price * (1 - 18 / 100)  # Stop loss at 18%
        take_profit = entry_price * (1 + 3 / 100)  # Take profit at 3%

        # print
        print(f"Breakout detected for {symbol}: Entry Price: {entry_price}, SL: {stop_loss}, TP: {take_profit}")

        # Check if SL < entry price < TP
        if stop_loss < entry_price < take_profit:
            return {
                'Symbol': symbol,
                'Entry Price': entry_price,
                'Stop Loss': stop_loss,
                'Take Profit': take_profit
            }
    return None


import pandas as pd
import numpy as np

def calculate_sma(data, period):
    return data['close'].rolling(window=period).mean()

# Mean reversion strategy function
def mean_reversion_strategy(symbol, data, sma_period, buy_range, sell_range):
    # Calculate SMA
    data['SMA'] = calculate_sma(data, sma_period)
    print(data)  # For debugging; you may remove this later

    # Ensure there are enough data points after calculating SMA
    if len(data) < sma_period:
        print(f"Not enough data to calculate SMA for period {sma_period}")
        return "HOLD", None, None, None

    # Get the last valid SMA value (non-NaN)
    last_valid_sma = data['SMA'].dropna().iloc[-1]

    # Calculate buying and selling thresholds
    buy_threshold = last_valid_sma * (1 - np.random.uniform(buy_range[0], buy_range[1]) / 100)
    sell_threshold = last_valid_sma * (1 + np.random.uniform(sell_range[0], sell_range[1]) / 100)

    # Get the latest closing price
    current_price = data['close'].iloc[-1]

    # Convert numpy numbers of current_price, buy_threshold, and sell_threshold to float
    current_price = float(current_price)
    buy_threshold = float(buy_threshold)
    sell_threshold = float(sell_threshold)

    # Strategy: Buy if current price is below the buy threshold; Sell if current price is above the sell threshold
    if current_price < buy_threshold:
        action = "BUY"
    elif current_price > sell_threshold:
        action = "SELL"
    else:
        action = "HOLD"

    return action, buy_threshold, sell_threshold, current_price


def main():
    # GET BALANCES FROM ACCT 1, SIZE, POSITION, ENTRY PRICE, PNL, LONG/SHORT
    account1 = LocalAccount = eth_account.Account.from_key(secret)

    for symbol in symbols:
        # Fetch the OHLCV data
        snapshot_data = n.get_ohlcv2(symbol, timeframe, 20)
        hourly_snapshots = n.process_data_to_df(snapshot_data)
        print(hourly_snapshots)

        if not hourly_snapshots.empty:
            # Fetch symbol-specific settings
            sma_period = symbols_data[symbol]['sma_period']
            buy_range = symbols_data[symbol]['buy_range']
            sell_range = symbols_data[symbol]['sell_range']
            
            # Run the mean reversion strategy
            action, buy_threshold, sell_threshold, current_price = mean_reversion_strategy(
                symbol, hourly_snapshots, sma_period, buy_range, sell_range
            )

            print(f"{symbol} - Action: {action}, Buy Threshold: {buy_threshold}, Sell Threshold: {sell_threshold}, Current Price: {current_price}")

            # action = 'BUY'
            if action == "BUY":
                print(f"Executing BUY order for {symbol}")
                print(f'passing {symbol} to adjust leverage and open order...')
                lev, size = n.adjust_leverage_usd_size(symbol, order_usd_size, leverage, account1)
                
                # check if we have a position of that symbol 
                positions, im_in_pos, pos_size, pos_sym, entry_px, pnl_perc, long = n.get_position(symbol, account1)
                
                if not im_in_pos:
                    print(f'not in position for {symbol}')
                    entry_price = current_price  # Set entry price as the current price
                    # rount entry proce to 3
                    entry_price = round(entry_price, 3)
                    # flaot it
                    entry_price = float(entry_price)

                    # same for buy threshold and sell threshold
                    buy_threshold = round(buy_threshold, 3)
                    buy_threshold = float(buy_threshold)

                    sell_threshold = round(sell_threshold, 3)
                    sell_threshold = float(sell_threshold)
                    
                    # Create a dictionary to hold the symbol information before sending the order
                    symbol_info = {
                        "Symbol": symbol,
                        "Entry Price": buy_threshold,
                        "Stop Loss": buy_threshold*.3,  # Assuming buy threshold is the stop loss for simplicity
                        "Take Profit": sell_threshold  # Similarly, assuming sell threshold for take profit
                    }
                    
                    n.open_order_deluxe(symbol_info, size, account1)
                    print(f"Order opened for {symbol}")
                    
                else:
                    print(f'already in a position for {symbol}')
                
            elif action == "SELL":
                print(f"Flashing SELL for {symbol} but we should already have the orders in place")
                # Place your sell order logic here
            else:
                print(f'we aint doin nothing but holding king')
                

print('running algo...')
main()
schedule.every(1).minutes.do(main)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"Encountered an error: {e}")
        time.sleep(10)