"""
General Database Functions for Mean Reversion Trading System

Provides database connection and OHLCV data fetching from the
MoonView PostgreSQL database (crypto.binance_candles table).
"""

import psycopg2
import pandas as pd
import sys
import os

# Add project root to path for credentials import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from credentials.api_secrets import DB_CONFIG


def get_db_connection():
    """
    Establish connection to PostgreSQL database.

    Returns:
        psycopg2 connection object or None if connection fails
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG.get('password', ''),
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
        pandas DataFrame with OHLCV data formatted for backtesting.py
        Columns: Open, High, Low, Close, Volume (capitalized)
        Index: timestamp (timezone-naive)
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


def check_available_data(granularity, timeframe_label='4h'):
    """
    Check what data is available in the database for a given granularity.

    Args:
        granularity: Timeframe in seconds (e.g., 14400 for 4h)
        timeframe_label: Human-readable label (e.g., '4h', '1h')

    Returns:
        pandas DataFrame with available symbols and their data ranges
    """
    conn = get_db_connection()
    if conn is None:
        return None

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

        df = pd.read_sql_query(query, conn, params=(granularity,))

        if df.empty:
            print(f"No {timeframe_label} data found in database.")
            print("Run the moonview data pull first:")
            print(f"  cd ~/WorkLocal/moonview && ./streamline/run_xchange.sh --timeframes {timeframe_label}")
        else:
            print(f"\nAvailable {timeframe_label} data in database:")
            print("-" * 80)
            print(df.to_string(index=False))
            print("-" * 80)

        return df

    except Exception as e:
        print(f"Error checking data: {e}")
        return None
    finally:
        conn.close()


def get_available_symbols(granularity=14400, conversion='USDT'):
    """
    Get list of available symbols for a given granularity.

    Args:
        granularity: Timeframe in seconds (default: 14400 for 4h)
        conversion: Quote currency (default: 'USDT')

    Returns:
        List of symbol strings
    """
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        query = """
            SELECT DISTINCT symbol
            FROM crypto.binance_candles
            WHERE granularity = %s AND conversion = %s
            ORDER BY symbol
        """

        df = pd.read_sql_query(query, conn, params=(granularity, conversion))
        return df['symbol'].tolist()

    except Exception as e:
        print(f"Error getting symbols: {e}")
        return []
    finally:
        conn.close()


# Granularity constants (timeframe in seconds)
GRANULARITY_1M = 60
GRANULARITY_5M = 300
GRANULARITY_15M = 900
GRANULARITY_1H = 3600
GRANULARITY_4H = 14400
GRANULARITY_6H = 21600
GRANULARITY_1D = 86400
