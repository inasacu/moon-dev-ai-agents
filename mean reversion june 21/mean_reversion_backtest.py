"""
Mean Reversion Backtesting Script

Connects to the MoonView PostgreSQL database to fetch latest OHLCV data
for BTC and ETH, then runs backtesting optimization to find optimal parameters.

Database: PostgreSQL (localhost:5432/postgres)
Schema: crypto
Table: binance_candles
"""

import numpy as np
from backtesting import Backtest, Strategy
from backtesting.test import SMA
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os

# Import database functions
from general_database_functions import (
    fetch_ohlcv_from_db,
    check_available_data,
    GRANULARITY_4H
)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Backtesting configuration
SYMBOL = 'BTC'              # Symbol to backtest: 'BTC' or 'ETH'
TIMEFRAME = '4h'            # Timeframe
GRANULARITY = GRANULARITY_4H  # 4h in seconds (14400)
CANDLE_LIMIT = 1000         # Number of candles (~6 months of 4h data)
CONVERSION = 'USDT'         # Quote currency

# Backtest settings
INITIAL_CASH = 100000       # Starting capital
COMMISSION = 0.002          # 0.2% commission (Binance futures)

# Optimization ranges
SMA_RANGE = range(10, 21)       # SMA periods to test (10-20)
BUY_PCT_RANGE = range(5, 20)    # Buy % below SMA (5-19%)
SELL_PCT_RANGE = range(5, 20)   # Sell % above SMA (5-19%)

# =============================================================================
# STRATEGY
# =============================================================================

class SMABuySellStrategy(Strategy):
    """
    Mean Reversion Strategy using SMA.

    - BUY when price drops below SMA by buy_pct%
    - SELL (close position) when price rises above SMA by sell_pct%
    """
    sma_period = 14  # Default SMA period, will be optimized
    buy_pct = 1.0    # Default buy percentage below SMA, will be optimized
    sell_pct = 1.0   # Default sell percentage above SMA, will be optimized

    def init(self):
        # Calculate the SMA using the Close price and the sma_period
        self.sma = self.I(SMA, self.data.Close, self.sma_period)

    def next(self):
        # Calculate the buying and selling thresholds
        buy_threshold = self.sma[-1] * (1 - self.buy_pct / 100)
        sell_threshold = self.sma[-1] * (1 + self.sell_pct / 100)

        # If the Close price is below the buy threshold, buy
        if len(self.data.Close) > 0 and self.data.Close[-1] < buy_threshold:
            self.buy()

        # If the Close price is above the sell threshold, sell
        elif len(self.data.Close) > 0 and self.data.Close[-1] > sell_threshold:
            self.position.close()


# =============================================================================
# MAIN
# =============================================================================

def run_backtest(symbol='BTC'):
    """Run the backtest for a given symbol."""

    print(f"\n{'='*60}")
    print(f"MEAN REVERSION BACKTEST - {symbol}")
    print(f"{'='*60}")

    # Check available data first
    print("\nChecking database for available data...")
    check_available_data(GRANULARITY, TIMEFRAME)

    # Fetch data from database
    print(f"\nFetching {symbol} {TIMEFRAME} data from database...")
    data = fetch_ohlcv_from_db(symbol, GRANULARITY, CANDLE_LIMIT, CONVERSION)

    if data is None or data.empty:
        print(f"\nERROR: Could not fetch data for {symbol}")
        print("\nTo populate the database, run:")
        print(f"  cd ~/WorkLocal/moonview")
        print(f"  ./streamline/run_xchange.sh --symbols BTC ETH --timeframes 4h")
        return None

    # Create and configure the backtest
    print(f"\nRunning backtest with {len(data)} candles...")
    print(f"Initial cash: ${INITIAL_CASH:,}")
    print(f"Commission: {COMMISSION*100}%")

    bt = Backtest(data, SMABuySellStrategy, cash=INITIAL_CASH, commission=COMMISSION)

    # Optimization with heatmap
    print(f"\nOptimizing parameters...")
    print(f"  SMA period: {SMA_RANGE.start}-{SMA_RANGE.stop-1}")
    print(f"  Buy %: {BUY_PCT_RANGE.start}-{BUY_PCT_RANGE.stop-1}%")
    print(f"  Sell %: {SELL_PCT_RANGE.start}-{SELL_PCT_RANGE.stop-1}%")

    opt_stats, heatmap = bt.optimize(
        sma_period=SMA_RANGE,
        buy_pct=BUY_PCT_RANGE,
        sell_pct=SELL_PCT_RANGE,
        maximize='Equity Final [$]',
        constraint=lambda param: param.sma_period > 0 and param.buy_pct > 0 and param.sell_pct > 0,
        return_heatmap=True,
    )

    # Print the optimization results
    print(f"\n{'='*60}")
    print("OPTIMIZATION RESULTS")
    print(f"{'='*60}")
    print(opt_stats)

    # Print best parameters
    print(f"\n{'='*60}")
    print("BEST PARAMETERS FOUND")
    print(f"{'='*60}")
    print(f"  SMA Period: {opt_stats._strategy.sma_period}")
    print(f"  Buy %: {opt_stats._strategy.buy_pct}% below SMA")
    print(f"  Sell %: {opt_stats._strategy.sell_pct}% above SMA")
    print(f"\n  Final Equity: ${opt_stats['Equity Final [$]']:,.2f}")
    print(f"  Return: {opt_stats['Return [%]']:.2f}%")
    print(f"  Max Drawdown: {opt_stats['Max. Drawdown [%]']:.2f}%")
    print(f"  Win Rate: {opt_stats['Win Rate [%]']:.2f}%")
    print(f"  # Trades: {opt_stats['# Trades']}")

    # Convert heatmap data to a 2D DataFrame for plotting
    try:
        heatmap_df = heatmap.unstack(level='buy_pct').T

        # Plot the heatmap for the optimization results
        plt.figure(figsize=(12, 10))
        sns.heatmap(heatmap_df, annot=True, fmt=".0f", cmap='viridis')
        plt.title(f"{symbol} Mean Reversion Optimization Heatmap\nFinal Equity by Buy/Sell Percentage")
        plt.xlabel("Sell Percentage (%)")
        plt.ylabel("Buy Percentage (%)")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not generate heatmap: {e}")

    # Run the backtest with the best parameters
    print(f"\nRunning backtest with optimal parameters...")
    results = bt.run(
        sma_period=opt_stats._strategy.sma_period,
        buy_pct=opt_stats._strategy.buy_pct,
        sell_pct=opt_stats._strategy.sell_pct
    )

    # Plot the performance
    try:
        bt.plot()
    except Exception as e:
        print(f"Could not generate plot: {e}")

    return opt_stats


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # You can change the symbol here or pass as command line argument
    symbol = SYMBOL

    if len(sys.argv) > 1:
        symbol = sys.argv[1].upper()

    print("\n" + "="*60)
    print("MEAN REVERSION BACKTESTER")
    print("Data Source: MoonView PostgreSQL Database")
    print("="*60)

    # Run backtest for the symbol
    results = run_backtest(symbol)

    # Optionally run for ETH as well (only in interactive mode)
    if symbol == 'BTC' and sys.stdin.isatty():
        print("\n" + "="*60)
        run_eth = input("\nRun backtest for ETH as well? (y/n): ").lower().strip()
        if run_eth == 'y':
            run_backtest('ETH')
