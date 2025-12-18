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
import psycopg2
import sys
import os

# Add project root to path for credentials import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =============================================================================
# CONFIGURATION
# =============================================================================

# Database configuration (matches moonview setup)
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'padilla',
    'password': '',
    'host': 'localhost',
    'port': 5432
}

# Backtesting configuration
SYMBOL = 'BTC'              # Symbol to backtest: 'BTC' or 'ETH'
TIMEFRAME = '4h'            # Timeframe
GRANULARITY = 14400         # 4h in seconds (4 * 60 * 60)
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
# DATABASE FUNCTIONS
# =============================================================================

def get_db_connection():
    """Establish connection to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        print("Make sure PostgreSQL is running and the database exists.")
        return None


def fetch_ohlcv_from_db(symbol, granularity, limit, conversion='USDT'):
    """
    Fetch OHLCV data from the crypto.binance_candles table.

    Args:
        symbol: Crypto symbol (e.g., 'BTC', 'ETH')
        granularity: Timeframe in seconds (14400 for 4h)
        limit: Number of candles to fetch
        conversion: Quote currency (default: 'USDT')

    Returns:
        pandas DataFrame with OHLCV data
    """
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        query = """
            SELECT
                timestamp,
                open,
                high,
                low,
                close,
                volume
            FROM crypto.binance_candles
            WHERE symbol = %s
              AND granularity = %s
              AND conversion = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(symbol, granularity, conversion, limit)
        )

        if df.empty:
            print(f"No data found for {symbol} with granularity {granularity}")
            print(f"Try running the moonview data pull first:")
            print(f"  cd ~/WorkLocal/moonview && ./streamline/run_xchange.sh --symbols {symbol} --timeframes 4h")
            return None

        # Sort by timestamp ascending (oldest first)
        df = df.sort_values('timestamp')

        # Set timestamp as index (convert timezone-aware to UTC then drop timezone)
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True).dt.tz_localize(None)
        df.set_index('timestamp', inplace=True)

        # Rename columns to match backtesting.py requirements
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        # Convert to float
        for col in df.columns:
            df[col] = df[col].astype(float)

        print(f"Fetched {len(df)} candles for {symbol}")
        print(f"Date range: {df.index.min()} to {df.index.max()}")

        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        conn.close()


def check_available_data():
    """Check what data is available in the database."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        query = """
            SELECT
                symbol,
                conversion,
                granularity,
                COUNT(*) as candle_count,
                MIN(timestamp) as earliest,
                MAX(timestamp) as latest
            FROM crypto.binance_candles
            WHERE granularity = %s
            GROUP BY symbol, conversion, granularity
            ORDER BY symbol
        """

        df = pd.read_sql_query(query, conn, params=(GRANULARITY,))

        if df.empty:
            print(f"No {TIMEFRAME} data found in database.")
            print("Run the moonview data pull first:")
            print("  cd ~/WorkLocal/moonview && ./streamline/run_xchange.sh --timeframes 4h")
        else:
            print(f"\nAvailable {TIMEFRAME} data in database:")
            print("-" * 80)
            print(df.to_string(index=False))
            print("-" * 80)

        return df

    except Exception as e:
        print(f"Error checking data: {e}")
        return None
    finally:
        conn.close()


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
    check_available_data()

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
