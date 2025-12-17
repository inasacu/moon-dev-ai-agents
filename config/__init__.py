"""
Configuration file for Moon Dev AI Agents project.
Synced from MoonView project - contains global constants and settings.
Last sync: 2025-12-17

## Data Structure
Common fields across all sources:
- `symbol` (varchar): Trading pair symbol (e.g., 'BTC-USD' for Coinbase, 'BTCUSDT' for Binance)
- `timestamp` (timestamp with timezone): The start time of the candle
- `low` (numeric): Lowest price during the period
- `high` (numeric): Highest price during the period
- `open` (numeric): Opening price
- `close` (numeric): Closing price
- `volume` (numeric): Trading volume
- `granularity` (integer): Timeframe in seconds
- `source` (varchar): Data source name ('binance', 'coinbase', 'hyperliquid')

## Timeframes and Historical Periods
- 1-minute (1m): Up to 90 days
- 5-minute (5m): Up to 90 days
- 15-minute (15m): Up to 90 days
- 1-hour (1h): Up to 365 days
- 4-hour (4h) / 6-hour (6h): Up to 365 days
- 1-day (1d): Multiple periods (30, 60, 90, 180, 270, 365, 5000 days)
"""

from pathlib import Path
from typing import Any, Dict, List, Literal, TypeVar, Union
from datetime import datetime

def clamp_usd_size(value):
    """
    Clamp and round usd_size to fit NUMERIC(20, 2) field: max 999999999999999999.99
    """
    max_usd_size = 999999999999999999.99
    try:
        return min(round(float(value), 2), max_usd_size)
    except Exception:
        return 0.0

def clamp_usd_size_millions(value):
    """
    Clamp and round usd_size_millions to fit NUMERIC(10, 2) field: max 99999999.99
    """
    max_usd_size_millions = 99999999.99
    try:
        return min(round(float(value), 2), max_usd_size_millions)
    except Exception:
        return 0.0


def clamp_numeric_20_10(value):
    """
    Clamp and round values to fit NUMERIC(20, 10) fields: max 9999999999.9999999999

    Used for price and quantity fields in hybrid_trades, whale_orders, liquidations, etc.
    NUMERIC(20, 10) means 20 total digits with 10 after decimal, leaving 10 before decimal.
    Maximum absolute value is 10^10 - 1 = 9,999,999,999.9999999999

    For tokens with extreme quantities (e.g., SHIB, PEPE with trillions of units),
    this clamping prevents "numeric field overflow" database errors.
    """
    max_value = 9999999999.9999999999
    try:
        return min(round(float(value), 10), max_value)
    except Exception:
        return 0.0


# =========================
# PATH CONFIGURATIONS
# =========================
# Note: .parent.parent because this file is now in config/ folder
MOONVIEW_PATH = Path(__file__).resolve().parent.parent
PROJECT_PATH = MOONVIEW_PATH  # Alias for this project

# =========================
# FEATURE FLAGS
# =========================
SUPABASE_ENABLED = False
DB_ENABLED = True
CSV_ENABLED = False
HTML_ENABLED = False
DATA_ONLY_ENABLED = False
DEBUG_ENABLED = False
ARCHIVE_ENABLED = False
CLEAN_DATABASE = False
TRUNCATE_CANDLES = False
RUN_ONCE_ENABLED = False
ENABLE_ETH = True
ENABLE_SOL = True
QUERY_BLOCKCHAINS = True
SYMBOLS_ALL_ENABLED = True

# =========================
# WALLET & WHALE CONFIGURATIONS
# =========================
WHALE_THRESHOLD = 1000  # BTC
LARGE_TX_THRESHOLD = 250000  # $250,000 USD
REFRESH_INTERVAL = 300  # 5 minutes
REFRESH_WALLET_INTERVAL = 300  # 5 minutes
DEFAULT_DISPLAY_THRESHOLD_USD = 10_000_000  # $10 million
DEFAULT_UPDATE_INTERVAL = 3600  # 1 hour
LARGE_WALLET_MINIMUM = 500_000  # $1 million minimum for large wallet tracking
MAX_DISPLAY_WALLETS = 25
REGULAR_LIQUIDATION_THRESHOLD = 50  # $50 minimum for regular liquidations (TESTING - normally 5000)
LARGE_LIQUIDATION_THRESHOLD = 10000  # $10K minimum for large liquidations (TESTING - normally 100000)
STATS_INTERVAL = 3600  # 1 hour for stats updates
TRACK_LARGE_LIQUIDATIONS = True  # Track liquidations >= $100K
TRACK_REGULAR_LIQUIDATIONS = True  # Track liquidations >= $5K
BOLD_LARGE_THRESHOLD = 100000  # Bold text for liquidations >= $100K
SUMMARY_DIVIDER_LENGTH = 70
BILLION_DISPLAY_THRESHOLD = 1_000_000_000  # $1B

# Folder Structure
FOLDER_CONFIG = {
    "csv": MOONVIEW_PATH / "data" / "raw" / "csv",
    "html": MOONVIEW_PATH / "data" / "raw" / "html",
    "results": MOONVIEW_PATH / "data" / "raw" / "results",
    "txt": MOONVIEW_PATH / "data" / "raw" / "txt",
    "whales": MOONVIEW_PATH / "data" / "raw" / "whales",
    "archive": MOONVIEW_PATH / "data" / "archive",
    # RBI (Research, Backtest, Implement) directories
    "rbi_strategies": MOONVIEW_PATH / "data" / "raw" / "rbi" / "strategies",
    "rbi_backtest": MOONVIEW_PATH / "data" / "raw" / "rbi" / "bt_code",
    "rbi_ids": MOONVIEW_PATH / "data" / "raw" / "rbi" / "ids",
    "rbi_results": MOONVIEW_PATH / "data" / "raw" / "rbi" / "results",
    "rbi_data": MOONVIEW_PATH / "data" / "raw" / "rbi" / "data",
}

# Quick access to folder paths
DEFAULT_CSV_DIR = FOLDER_CONFIG["csv"]
DEFAULT_HTML_DIR = FOLDER_CONFIG["html"]
DEFAULT_RESULTS_DIR = FOLDER_CONFIG["results"]
DEFAULT_TXT_DIR = FOLDER_CONFIG["txt"]
DEFAULT_WHALE_DIR = FOLDER_CONFIG["whales"]
DEFAULT_ARCHIVE_DIR = FOLDER_CONFIG["archive"]
RBI_STRATEGIES_DIR = FOLDER_CONFIG["rbi_strategies"]
RBI_BACKTEST_DIR = FOLDER_CONFIG["rbi_backtest"]
RBI_IDS_DIR = FOLDER_CONFIG["rbi_ids"]
RBI_RESULTS_DIR = FOLDER_CONFIG["rbi_results"]
RBI_DATA_DIR = FOLDER_CONFIG["rbi_data"]

# Log directory
LOG_DIR = MOONVIEW_PATH / "logs"

# =========================
# TYPE DEFINITIONS
# =========================
PathLike = Union[str, Path]
JsonData = Union[Dict[str, Any], List[Any], str, int, float, bool, None]
T = TypeVar("T")

TERMCOLOR = Literal[
    "grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta",
    "on_cyan", "on_white", "on_light_green", "on_dark_grey", "on_black",
    "bold", "dark", "underline", "blink", "reverse", "concealed"
]

# =========================
# CRYPTOCURRENCY METADATA (MAIN SOURCE)
# =========================
REFERENCE_DATE = datetime.now()

# =============================================================================
# CRYPTO_METADATA - Active Coins (20 coins sorted by market cap)
# Last updated: 2025-12-17
# =============================================================================
CRYPTO_METADATA = {
    # === TOP 20 BY MARKET CAP ===
    "BTC": {
        "name": "Bitcoin",
        "symbol": "BTC",
        "launch_date": datetime(2009, 1, 3),
        "type": "Crypto Coin",
        "emoji": "💰",
        "decimal_places": 8,
        "api_path": "bitcoin",
        "conversion_factor": 100000000,
        "age_days": (REFERENCE_DATE - datetime(2009, 1, 3)).days,
        "priority": 1,
        "symbols": {
            "binance": "BTC/USDT",
            "coinbase": "BTC/USD",
            "hyperliquid": "BTC/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "ETH": {
        "name": "Ethereum",
        "symbol": "ETH",
        "launch_date": datetime(2015, 7, 30),
        "type": "Crypto Coin",
        "emoji": "💎",
        "decimal_places": 18,
        "api_path": "ethereum",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2015, 7, 30)).days,
        "priority": 2,
        "symbols": {
            "binance": "ETH/USDT",
            "coinbase": "ETH/USD",
            "hyperliquid": "ETH/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "BNB": {
        "name": "Binance Coin",
        "symbol": "BNB",
        "launch_date": datetime(2017, 7, 1),
        "type": "Crypto Coin",
        "emoji": "🔥",
        "decimal_places": 18,
        "api_path": "binancecoin",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2017, 7, 1)).days,
        "priority": 3,
        "symbols": {
            "binance": "BNB/USDT",
            "hyperliquid": "BNB/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "XRP": {
        "name": "XRP",
        "symbol": "XRP",
        "launch_date": datetime(2013, 4, 1),
        "type": "Crypto Coin",
        "emoji": "💧",
        "decimal_places": 6,
        "api_path": "ripple",
        "conversion_factor": 1000000,
        "age_days": (REFERENCE_DATE - datetime(2013, 4, 1)).days,
        "priority": 4,
        "symbols": {
            "binance": "XRP/USDT",
            "coinbase": "XRP/USD",
            "hyperliquid": "XRP/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "SOL": {
        "name": "Solana",
        "symbol": "SOL",
        "launch_date": datetime(2020, 4, 1),
        "type": "Crypto Coin",
        "emoji": "🧬",
        "decimal_places": 9,
        "api_path": "solana",
        "conversion_factor": 1000000000,
        "age_days": (REFERENCE_DATE - datetime(2020, 4, 1)).days,
        "priority": 5,
        "symbols": {
            "binance": "SOL/USDT",
            "coinbase": "SOL/USD",
            "hyperliquid": "SOL/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "TRX": {
        "name": "Tron",
        "symbol": "TRX",
        "launch_date": datetime(2017, 9, 1),
        "type": "Crypto Coin",
        "emoji": "⚡",
        "decimal_places": 6,
        "api_path": "tron",
        "conversion_factor": 1000000,
        "age_days": (REFERENCE_DATE - datetime(2017, 9, 1)).days,
        "priority": 6,
        "symbols": {
            "binance": "TRX/USDT",
            "coinbase": "TRX/USD",
            "hyperliquid": "TRX/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "ADA": {
        "name": "Cardano",
        "symbol": "ADA",
        "launch_date": datetime(2017, 9, 1),
        "type": "Crypto Coin",
        "emoji": "🧠",
        "decimal_places": 6,
        "api_path": "cardano",
        "conversion_factor": 1000000,
        "age_days": (REFERENCE_DATE - datetime(2017, 9, 1)).days,
        "priority": 7,
        "symbols": {
            "binance": "ADA/USDT",
            "coinbase": "ADA/USD",
            "hyperliquid": "ADA/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "LINK": {
        "name": "Chainlink",
        "symbol": "LINK",
        "launch_date": datetime(2017, 9, 1),
        "type": "Crypto Coin",
        "emoji": "🔗",
        "decimal_places": 18,
        "api_path": "chainlink",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2017, 9, 1)).days,
        "priority": 8,
        "symbols": {
            "binance": "LINK/USDT",
            "coinbase": "LINK/USD",
            "hyperliquid": "LINK/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "XMR": {
        "name": "Monero",
        "symbol": "XMR",
        "launch_date": datetime(2014, 4, 18),
        "type": "Crypto Coin",
        "emoji": "🔒",
        "decimal_places": 12,
        "api_path": "monero",
        "conversion_factor": 1000000000000,
        "age_days": (REFERENCE_DATE - datetime(2014, 4, 18)).days,
        "priority": 9,
        "symbols": {
            # Note: XMR delisted from most major exchanges, limited availability
        },
        "exchange_timeframes": {}
    },
    "HYPE": {
        "name": "Hyperliquid",
        "symbol": "HYPE",
        "launch_date": datetime(2024, 11, 29),
        "type": "Crypto Coin",
        "emoji": "🚀",
        "decimal_places": 18,
        "api_path": "hyperliquid",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2024, 11, 29)).days,
        "priority": 10,
        "symbols": {
            "hyperliquid": "HYPE/USDC:USDC"
        },
        "exchange_timeframes": {
            "hyperliquid": "DEFAULT"
        }
    },
    "SUI": {
        "name": "Sui",
        "symbol": "SUI",
        "launch_date": datetime(2023, 5, 1),
        "type": "Crypto Coin",
        "emoji": "💧",
        "decimal_places": 9,
        "api_path": "sui",
        "conversion_factor": 1000000000,
        "age_days": (REFERENCE_DATE - datetime(2023, 5, 1)).days,
        "priority": 11,
        "symbols": {
            "binance": "SUI/USDT",
            "coinbase": "SUI/USD",
            "hyperliquid": "SUI/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "MNT": {
        "name": "Mantle",
        "symbol": "MNT",
        "launch_date": datetime(2023, 7, 1),
        "type": "Crypto Coin",
        "emoji": "🏔️",
        "decimal_places": 18,
        "api_path": "mantle",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2023, 7, 1)).days,
        "priority": 12,
        "symbols": {
            "binance": "MNT/USDT",
            "hyperliquid": "MNT/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "UNI": {
        "name": "Uniswap",
        "symbol": "UNI",
        "launch_date": datetime(2020, 9, 1),
        "type": "Crypto Coin",
        "emoji": "🦄",
        "decimal_places": 18,
        "api_path": "uniswap",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2020, 9, 1)).days,
        "priority": 13,
        "symbols": {
            "binance": "UNI/USDT",
            "coinbase": "UNI/USD",
            "hyperliquid": "UNI/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "DOT": {
        "name": "Polkadot",
        "symbol": "DOT",
        "launch_date": datetime(2020, 5, 1),
        "type": "Crypto Coin",
        "emoji": "🎯",
        "decimal_places": 10,
        "api_path": "polkadot",
        "conversion_factor": 10000000000,
        "age_days": (REFERENCE_DATE - datetime(2020, 5, 1)).days,
        "priority": 14,
        "symbols": {
            "binance": "DOT/USDT",
            "coinbase": "DOT/USD",
            "hyperliquid": "DOT/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "AAVE": {
        "name": "Aave",
        "symbol": "AAVE",
        "launch_date": datetime(2017, 11, 1),
        "type": "Crypto Coin",
        "emoji": "🏦",
        "decimal_places": 18,
        "api_path": "aave",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2017, 11, 1)).days,
        "priority": 15,
        "symbols": {
            "binance": "AAVE/USDT",
            "coinbase": "AAVE/USD",
            "hyperliquid": "AAVE/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "OKB": {
        "name": "OKB",
        "symbol": "OKB",
        "launch_date": datetime(2019, 4, 1),
        "type": "Crypto Coin",
        "emoji": "🔷",
        "decimal_places": 18,
        "api_path": "okb",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2019, 4, 1)).days,
        "priority": 16,
        "symbols": {
            # Note: OKB primarily trades on OKX exchange
            "hyperliquid": "OKB/USDC:USDC"
        },
        "exchange_timeframes": {
            "hyperliquid": "DEFAULT"
        }
    },
    "ICP": {
        "name": "Internet Computer",
        "symbol": "ICP",
        "launch_date": datetime(2021, 5, 10),
        "type": "Crypto Coin",
        "emoji": "🌐",
        "decimal_places": 8,
        "api_path": "internet-computer",
        "conversion_factor": 100000000,
        "age_days": (REFERENCE_DATE - datetime(2021, 5, 10)).days,
        "priority": 17,
        "symbols": {
            "binance": "ICP/USDT",
            "coinbase": "ICP/USD",
            "hyperliquid": "ICP/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "ENA": {
        "name": "Ethena",
        "symbol": "ENA",
        "launch_date": datetime(2024, 4, 2),
        "type": "Crypto Coin",
        "emoji": "💠",
        "decimal_places": 18,
        "api_path": "ethena",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2024, 4, 2)).days,
        "priority": 18,
        "symbols": {
            "binance": "ENA/USDT",
            "hyperliquid": "ENA/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
    "SKY": {
        "name": "Sky",
        "symbol": "SKY",
        "launch_date": datetime(2024, 9, 18),
        "type": "Crypto Coin",
        "emoji": "☁️",
        "decimal_places": 18,
        "api_path": "sky",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2024, 9, 18)).days,
        "priority": 19,
        "symbols": {
            # Note: SKY is rebranded MakerDAO, limited exchange support initially
            "hyperliquid": "SKY/USDC:USDC"
        },
        "exchange_timeframes": {
            "hyperliquid": "DEFAULT"
        }
    },
    "ARB": {
        "name": "Arbitrum",
        "symbol": "ARB",
        "launch_date": datetime(2021, 8, 1),
        "type": "Crypto Coin",
        "emoji": "🌉",
        "decimal_places": 18,
        "api_path": "arbitrum",
        "conversion_factor": 1000000000000000000,
        "age_days": (REFERENCE_DATE - datetime(2021, 8, 1)).days,
        "priority": 20,
        "symbols": {
            "binance": "ARB/USDT",
            "coinbase": "ARB/USD",
            "hyperliquid": "ARB/USDC:USDC"
        },
        "exchange_timeframes": {
            "binance": "DEFAULT",
            "coinbase": "DEFAULT",
            "hyperliquid": "DEFAULT"
        }
    },
}

# =============================================================================
# ARCHIVED COINS - Commented out for possible future redeployment
# =============================================================================
# "DOGE": {
#     "name": "Dogecoin",
#     "symbol": "DOGE",
#     "launch_date": datetime(2013, 12, 6),
#     "type": "Crypto Coin",
#     "emoji": "🐶",
#     "decimal_places": 8,
#     "api_path": "dogecoin",
#     "conversion_factor": 100000000,
#     "priority": 99,
#     "symbols": {"binance": "DOGE/USDT", "coinbase": "DOGE/USD", "hyperliquid": "DOGE/USDC:USDC"}
# },
# "SHIB": {
#     "name": "Shiba Inu",
#     "symbol": "SHIB",
#     "launch_date": datetime(2020, 8, 1),
#     "type": "Crypto Coin",
#     "emoji": "🦊",
#     "decimal_places": 18,
#     "api_path": "shiba-inu",
#     "conversion_factor": 1000000000000000000,
#     "priority": 99,
#     "symbols": {"binance": "SHIB/USDT", "coinbase": "SHIB/USD", "hyperliquid": "kSHIB/USDC:USDC"}
# },
# "MATIC": {
#     "name": "Polygon",
#     "symbol": "MATIC",
#     "launch_date": datetime(2017, 10, 1),
#     "type": "Crypto Coin",
#     "emoji": "🧩",
#     "decimal_places": 18,
#     "api_path": "matic-network",
#     "conversion_factor": 1000000000000000000,
#     "priority": 99,
#     "symbols": {}
# },
# "MKR": {
#     "name": "Maker",
#     "symbol": "MKR",
#     "launch_date": datetime(2017, 12, 1),
#     "type": "Crypto Coin",
#     "emoji": "🌐",
#     "decimal_places": 18,
#     "api_path": "maker",
#     "conversion_factor": 1000000000000000000,
#     "priority": 99,
#     "symbols": {"binance": "MKR/USDT", "coinbase": "MKR-USD"}
# },
# "CRV": {
#     "name": "Curve DAO",
#     "symbol": "CRV",
#     "launch_date": datetime(2020, 8, 1),
#     "type": "Crypto Coin",
#     "emoji": "🌍",
#     "decimal_places": 18,
#     "api_path": "curve-dao-token",
#     "conversion_factor": 1000000000000000000,
#     "priority": 99,
#     "symbols": {"binance": "CRV/USDT", "coinbase": "CRV-USD"}
# },
# "OP": {
#     "name": "Optimism",
#     "symbol": "OP",
#     "launch_date": datetime(2021, 12, 16),
#     "type": "Crypto Coin",
#     "emoji": "🧱",
#     "decimal_places": 18,
#     "api_path": "optimism",
#     "conversion_factor": 1000000000000000000,
#     "priority": 99,
#     "symbols": {"binance": "OP/USDT", "coinbase": "OP-USD"}
# },
# "PEPE": {
#     "name": "Pepe",
#     "symbol": "PEPE",
#     "launch_date": datetime(2023, 4, 1),
#     "type": "Crypto Coin",
#     "emoji": "🐸",
#     "decimal_places": 18,
#     "api_path": "pepe",
#     "conversion_factor": 1000000000000000000,
#     "priority": 99,
#     "symbols": {"binance": "PEPE/USDT", "coinbase": "PEPE-USD"}
# },
# "AI16Z": {
#     "name": "ai16z",
#     "symbol": "AI16Z",
#     "launch_date": datetime(2025, 1, 1),
#     "type": "Crypto Coin",
#     "emoji": "🤖",
#     "decimal_places": 18,
#     "api_path": "ai16z",
#     "conversion_factor": 1000000000000000000,
#     "priority": 99,
#     "symbols": {"binance": "AI16Z/USDT"}
# },
# "POPCAT": {
#     "name": "Popcat",
#     "symbol": "POPCAT",
#     "launch_date": datetime(2024, 1, 1),
#     "type": "Meme Coin",
#     "emoji": "🐱",
#     "decimal_places": 9,
#     "api_path": "popcat-sol",
#     "conversion_factor": 1000000000,
#     "priority": 99,
#     "symbols": {"binance": "POPCAT/USDT", "coinbase": "POPCAT-USD", "hyperliquid": "POPCAT/USDC:USDC"}
# },

# =========================
# HELPER FUNCTIONS
# =========================

def get_liquidation_stream_url(all_symbols: bool = True) -> str:
    """Build liquidation stream URL for Binance futures."""
    if all_symbols:
        return "wss://fstream.binance.com/ws/!forceOrder@arr"

    symbols = []
    for symbol, data in CRYPTO_METADATA.items():
        if "symbols" in data and "binance" in data["symbols"]:
            binance_symbol = data["symbols"]["binance"]
            futures_symbol = binance_symbol.replace("/", "").lower()
            symbols.append(f"{futures_symbol}@forceOrder")

    streams = "/".join(symbols)
    return f"wss://fstream.binance.com/stream?streams={streams}"

# =========================
# SUPABASE CONFIGURATIONS
# =========================
SUPABASE_MOONVIEW_URL = "postgresql://postgres:[YOUR-PASSWORD]@db.zvauawxcdmojjwrxfzqz.supabase.co:5432/postgres"
SUPABASE_POOLER_URL = "postgresql://postgres.zvauawxcdmojjwrxfzqz:[YOUR-PASSWORD]@aws-0-eu-west-3.pooler.supabase.com:6543/postgres"

# =========================
# API ENDPOINTS
# =========================
API_ENDPOINTS = {
    "binance": "https://api.binance.com/api/v3",
    "coinbase": "https://api.exchange.coinbase.com",
    "hyperliquid": "https://api.hyperliquid.xyz/info",
    "blockchain_raw":  "https://blockchain.info/rawaddr/",
    "blockchain": "https://blockchain.info/multiaddr?active=",
    "blockchain_info": "https://blockchain.info",
    "blockchair_api": "https://api.blockchair.com/ethereum/addresses",
    "etherscan_api": "https://api.etherscan.io/api",
    "coingecko": "https://api.coingecko.com/api/v3/simple/price",
    "solana_beta": "https://api.mainnet-beta.solana.com",
    "solana_rpc": "https://api.mainnet-beta.solana.com",
    "solscan_api": "https://public-api.solscan.io/account/",
    "projectserum": "https://solana-api.projectserum.com",
    "genesysgo": "https://ssc-dao.genesysgo.net",
    "websocket": "wss://stream.binance.com:9443",
    "websocket_stream_url": None,
    "futures_websocket": "wss://fstream.binance.com/ws/",
    "mempool": "https://blockchain.info/unconfirmed-transactions?format=json",
    "alchemy": "https://eth-mainnet.g.alchemy.com/v2/",
    "infura": "https://mainnet.infura.io/v3/",
    "cloudflare-eth": "https://cloudflare-eth.com",
    "beaconcha": "https://beaconcha.in/api/v1/epoch/latest",
}

# =========================
# EXCHANGE CONFIGURATIONS
# =========================
BLOCKCHAIN_URL = API_ENDPOINTS["blockchain"]
WEBSOCKET_URL = API_ENDPOINTS["websocket"]
WEBSOCKET_STREAM_URL = get_liquidation_stream_url()
FUTURES_WEBSOCKET_URL = API_ENDPOINTS["futures_websocket"]
BINANCE_API_URL = API_ENDPOINTS["binance"]
COINBASE_API_URL = API_ENDPOINTS["coinbase"]
HYPERLIQUID_URL = API_ENDPOINTS["hyperliquid"]
COINGECKO_URL = API_ENDPOINTS["coingecko"]
MEMPOOL_TX_URL = API_ENDPOINTS["mempool"]
BLOCKCHAIN_INFO_URL = API_ENDPOINTS["blockchain_info"]
ETHERSCAN_URL = API_ENDPOINTS["etherscan_api"]
SOLANA_BETA_URL = API_ENDPOINTS["solana_beta"]
SOLANA_API_URL = API_ENDPOINTS["solscan_api"]
SOLANA_RPC_URL = API_ENDPOINTS["solana_rpc"]
ALCHEMY_URL = API_ENDPOINTS["alchemy"]
INFURA_URL = API_ENDPOINTS["infura"]
CLOUDFLARE_ETH_URL = API_ENDPOINTS["cloudflare-eth"]
BEACONCHA_API_URL = API_ENDPOINTS["beaconcha"]
PROJECTSERUM_URL = API_ENDPOINTS["projectserum"]
GENESYSGO_URL = API_ENDPOINTS["genesysgo"]
BLOCKCHAIN_RAW_URL = API_ENDPOINTS["blockchain_raw"]

SOURCES = {
    "binance": {
        "enabled": True,
        "api_endpoint": API_ENDPOINTS["binance"],
        "max_candles": 1000,
        "websocket_url": API_ENDPOINTS["websocket"],
        "futures_websocket": API_ENDPOINTS["futures_websocket"],
    },
    "coinbase": {
        "enabled": True,
        "api_endpoint": API_ENDPOINTS["coinbase"],
        "max_candles": 300,
    },
    "hyperliquid": {
        "enabled": True,
        "api_endpoint": API_ENDPOINTS["hyperliquid"],
        "max_candles": 5000,
    },
}

# =========================
# TIMEFRAME CONFIGURATIONS
# =========================
TIMEFRAME_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "4h": 14400,
    "6h": 21600,
    "1d": 86400,
}

BASE_TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "6h", "1d"]

BASE_TIMEFRAME_CONFIG = {
    "1m": {"days": [90]},
    "5m": {"days": [90]},
    "15m": {"days": [90]},
    "1h": {"days": [365]},
    "4h": {"days": [365]},
    "6h": {"days": [365]},
    "1d": {"days": [30, 60, 90]},
}

COINBASE_TIMEFRAME_CONFIG = {
    "1m": {"days": [90]},
    "5m": {"days": [90]},
    "15m": {"days": [90]},
    "1h": {"days": [365]},
    "6h": {"days": [365]},
    "1d": {"days": [30, 60, 90]},
}

HYPERLIQUID_TIMEFRAME_CONFIG = {
    "1m": {"days": [90]},
    "5m": {"days": [90]},
    "15m": {"days": [90]},
    "1h": {"days": [365]},
    "4h": {"days": [365]},
    "1d": {"days": [30, 60, 90]},
}

# =========================
# TRADING CONFIGURATIONS
# =========================
def get_priority_symbols(max_priority: int = 6) -> list:
    """Get symbols with priority <= max_priority, sorted by priority."""
    return [
        symbol for symbol, data in sorted(
            CRYPTO_METADATA.items(),
            key=lambda x: x[1].get("priority", 999)
        )
        if data.get("priority", 999) <= max_priority
    ]

def get_symbols_by_type(crypto_type: str) -> list:
    """Get symbols filtered by cryptocurrency type."""
    return [
        symbol for symbol, data in CRYPTO_METADATA.items()
        if data.get("type", "") == crypto_type
    ]

BASE_SOURCES = ["binance", "coinbase", "hyperliquid"]
BASE_ALL_SYMBOLS = [
    symbol for symbol, data in CRYPTO_METADATA.items()
    if data.get("symbols", {})
]

if SYMBOLS_ALL_ENABLED:
    BASE_SYMBOLS = BASE_ALL_SYMBOLS
else:
    BASE_SYMBOLS = get_priority_symbols(6)

DEFAULT_SYMBOLS = {
    symbol.lower(): data["symbols"].get("binance", f"{symbol}USDT")
    for symbol, data in CRYPTO_METADATA.items()
    if data.get("priority", 999) <= 6 and "symbols" in data
}

# Wallet tiers configuration
WALLET_TIERS = [
    {"name": "mega_whale", "threshold_multiplier": 100, "text_color": "white", "back_color": "on_red", "indicator": "🐋🐋🐋 MEGA WHALE", "format_in_billions": True},
    {"name": "whale", "threshold_multiplier": 10, "text_color": "white", "back_color": "on_blue", "indicator": "🐋🐋 WHALE", "format_in_billions": False},
    {"name": "mini_whale", "threshold_multiplier": 1, "text_color": "white", "back_color": "on_blue", "indicator": "🐋 WHALE", "format_in_billions": False},
    {"name": "large_holder", "threshold_multiplier": 0.1, "text_color": "white", "back_color": "on_magenta", "indicator": "💰💰💰 LARGE HOLDER", "format_in_billions": False},
    {"name": "medium_holder", "threshold_multiplier": 0.025, "text_color": "white", "back_color": "on_green", "indicator": "💰💰 MEDIUM HOLDER", "format_in_billions": False},
    {"name": "small_holder", "threshold_multiplier": 0, "text_color": "white", "back_color": "on_cyan", "indicator": "💰 SMALL HOLDER", "format_in_billions": False},
]

TRADE_SIZE_INDICATOR_MAP = {
    "mega_whale": {"indicator": "🐋🐋🐋", "attrs": ["bold", "blink"], "desc": "$1M+ trades - Mega whale"},
    "whale": {"indicator": "🐋🐋", "attrs": ["bold"], "desc": "$500K-$1M trades - Whale"},
    "mini_whale": {"indicator": "🐋", "attrs": ["bold"], "desc": "$250K-$500K trades - Mini whale"},
    "large": {"indicator": "💰💰", "attrs": [], "desc": "$100K-$250K trades - Large"},
    "medium": {"indicator": "💰", "attrs": [], "desc": "$25K-$100K trades - Medium"},
    "small": {"indicator": "💵", "attrs": [], "desc": "$5K-$25K trades - Small"},
    "tiny": {"indicator": "", "attrs": [], "desc": "Below $5K - Tiny trade"},
}

CRYPTO_INDICATOR_THRESHOLDS = [
    (1000000, "🐋", 1, True),
    (500000, "🚀", 1, True),
    (250000, "💎", 1, True),
    (100000, "💰", 1, False),
    (25000, "💵", 1, False),
]

# =========================
# DATABASE CONFIGURATIONS
# =========================
DB_SCHEMA = "crypto"
DB_TABLE_TEMPLATE = "{source}_candles"

TRUNCATE_TABLES = {
    "binance": {"enabled": TRUNCATE_CANDLES, "name": "binance_candles"},
    "coinbase": {"enabled": TRUNCATE_CANDLES, "name": "coinbase_candles"},
    "hyperliquid": {"enabled": TRUNCATE_CANDLES, "name": "hyperliquid_candles"},
}

# Database config for connection pool
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "moonview",
    "user": "postgres",
    "password": "",
}

CONNECTION_POOL_CONFIG = {
    "min_connections": 1,
    "max_connections": 10,
}

# =========================
# REQUEST CONFIGURATIONS
# =========================
REQUEST_CONFIG = {
    "max_retries": 3,
    "base_delay": 2,
    "max_delay": 30,
    "timeout": 30,
    "max_workers": 5,
}

SAVE_OPTIONS = {"csv": CSV_ENABLED, "html": HTML_ENABLED, "database": DB_ENABLED}

# =========================
# DISPLAY & UI CONFIGURATIONS
# =========================
ICONS = {
    "success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️",
    "time": "⏱️", "data": "📊", "batch": "📦", "progress": "📈",
    "download": "⬇️", "calendar": "📅", "clock": "🕒", "crypto": "₿",
}

class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BACKGROUND = "\033[7m"
    BACKGREEN = "\033[42m"
    BACKBLUE = "\033[44m"
    BACKYELLOW = "\033[43m"
    REVERSED = "\033[7m"
    WHITE = "\033[97m"
    BACKRED = "\033[41m"
    BACKMAGENTA = "\033[45m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    ORANGE = "\033[38;5;208m"
    PURPLE = "\033[35m"
    GRAY = "\033[90m"
    BRIGHTRED = "\033[91m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

ATTR_MAP = {
    "bold": "\033[1m",
    "dark": "\033[2m",
    "underline": "\033[4m",
    "blink": "\033[5m",
    "reverse": "\033[7m",
    "concealed": "\033[8m",
}

BCH_COLORS = {
    "1m": Colors.BRIGHTRED, "3m": Colors.BRIGHTRED, "5m": Colors.YELLOW,
    "15m": Colors.GREEN, "30m": Colors.OKGREEN, "1h": Colors.BLUE,
    "2h": Colors.OKBLUE, "4h": Colors.PURPLE, "6h": Colors.HEADER,
    "1d": Colors.ORANGE, "3d": Colors.CYAN, "1w": Colors.WHITE,
}

WALLET_SYMBOLS = {"whale": "🐋", "regular": "💰"}

COLOR_CODING_TEMPLATE = [
    "Color coding:",
    "  RED: Mega whales (>{}M+)",
    "  BLUE: Whale wallets (>{}M+)",
    "  MAGENTA: Large wallets (>{}M+)",
    "  GREEN: Medium wallets (>{}M+)",
    "  CYAN: Smaller wallets (<{}M)",
    "\nSymbols:",
    "  {}: Whale wallet",
    "  {}: Regular wallet",
]

# =========================
# DATA HEADERS & FILE CONFIGURATIONS
# =========================
DEFAULT_DAILY_HEADERS = {
    "liquidation": ["Timestamp", "Symbol", "Side", "OrderType", "TimeInForce", "OriginalQuantity", "Price", "AveragePrice", "OrderStatus", "LastFilledQty", "FilledAccumQty", "TradeTime", "UsdSize", "DisplayTime"],
    "large_liquidation": ["Timestamp", "Symbol", "Side", "OrderType", "TimeInForce", "OriginalQuantity", "Price", "AveragePrice", "OrderStatus", "LastFilledQty", "FilledAccumQty", "TradeTime", "UsdSize", "UsdSizeMillion", "DisplayTime"],
    "whale_orders": ["Event Time", "Symbol", "Aggregate Trade ID", "Price", "Quantity", "First Trade ID", "Last Trade ID", "Trade Time", "Buyer Is Market Maker", "USD Size", "Trade Type"],
    "funding_rate": ["Timestamp", "Symbol", "Funding Rate", "Yearly Funding Rate", "Next Funding Time"],
}

FILENAME_PREFIXES = {
    "liquidation": "Liquidation_Data_Stream",
    "large_liquidation": "Large_Liquidation_Data_Stream",
    "whale_orders": "Whale_Orders_Tracker",
    "funding_rate": "Funding_Rate_Tracker",
}

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# =========================
# FUNDING RATE & LIQUIDATION CONFIGURATIONS
# =========================
INDICATOR_MAPPING = [
    (100, "white", "on_red", "!!!"),
    (50, "white", "on_magenta", "!!"),
    (30, "black", "on_yellow", "!"),
    (10, "black", "on_cyan", "^"),
    (0, "black", "on_light_green", "√"),
    (-10, "black", "on_green", "$"),
    (-30, "white", "on_blue", "$"),
    (float("-inf"), "white", "on_dark_grey", "$$"),
]

LIQUIDATION_COLOR_CODING = [
    "Color coding:",
    "  BLUE: Long liquidations (forced sells)",
    "  MAGENTA: Short liquidations (forced buys)",
]

DESCRIPTION_LINES = ["Minimum trade size: $5,000"]
DESCRIPTION_LIQUIDATION_LINES = DESCRIPTION_LINES.copy()
DESCRIPTION_LARGE_LINES = DESCRIPTION_LINES.copy()

# =========================
# HELPER FUNCTIONS
# =========================
COIN_ID_MAP = {}

POSITION_THRESHOLDS = {
    "mega_whale": 1000000,
    "whale": 500000,
    "mini_whale": 250000,
    "large": 100000,
    "medium": 25000,
    "small": 5000
}

def get_size_indicator(usd_size: float) -> str:
    """Get size indicator emoji"""
    if usd_size >= 1_000_000: return '🦈'
    elif usd_size >= 500_000: return '🐋'
    elif usd_size >= 250_000: return '🚀'
    elif usd_size >= 100_000: return '💎'
    elif usd_size >= 25_000: return '💰'
    else: return '💵'

def get_symbol_emoji(symbol):
    """Get emoji for cryptocurrency symbol"""
    crypto_info = CRYPTO_METADATA.get(symbol.upper(), {})
    return crypto_info.get('emoji', '🪙')

def get_trade_size_category(usd_size):
    """Determine the trade size category based on USD value"""
    if usd_size >= 1000000: return "mega_whale"
    elif usd_size >= 500000: return "whale"
    elif usd_size >= 250000: return "mini_whale"
    elif usd_size >= 100000: return "large"
    elif usd_size >= 25000: return "medium"
    elif usd_size >= 5000: return "small"
    else: return "micro"

def format_number(number, format_type='regular'):
    """Format numbers for display"""
    try:
        if format_type == 'price':
            return f"{float(number):,.2f}"
        elif format_type == 'value':
            number = float(number)
            if number >= 1_000_000_000: return f"${number / 1_000_000_000:.2f}B"
            elif number >= 1_000_000: return f"${number / 1_000_000:.2f}M"
            elif number >= 1_000: return f"${number / 1_000:.2f}K"
            return f"${number:.2f}"
        else:
            return f"{float(number):,.8f}"
    except (ValueError, TypeError):
        return "0.00"

def get_position_indicator(value: float) -> tuple:
    """Get emoji and attributes based on position value"""
    if value >= POSITION_THRESHOLDS["mega_whale"]: return "🐋🐋🐋", ['bold', 'blink']
    elif value >= POSITION_THRESHOLDS["whale"]: return "🐋🐋", ['bold']
    elif value >= POSITION_THRESHOLDS["mini_whale"]: return "🐋", ['bold']
    elif value >= POSITION_THRESHOLDS["large"]: return "💰💰", []
    elif value >= POSITION_THRESHOLDS["medium"]: return "💰", []
    else: return "💵", []

def get_crypto_info(symbol: str) -> dict:
    """Get cryptocurrency information by symbol."""
    return CRYPTO_METADATA.get(symbol.upper(), {})

def get_crypto_symbols(exchange: str | None = None) -> dict:
    """Get cryptocurrency symbols for specific exchange or all."""
    if exchange:
        return {symbol: data["symbols"].get(exchange, symbol) for symbol, data in CRYPTO_METADATA.items() if "symbols" in data and exchange in data["symbols"]}
    else:
        return {symbol: symbol for symbol in CRYPTO_METADATA.keys()}

def get_crypto_age(symbol: str) -> int:
    return get_crypto_info(symbol).get('age_days', 0)

def get_crypto_type(symbol: str) -> str:
    return get_crypto_info(symbol).get('type', 'Unknown')

def get_crypto_emoji(symbol: str) -> str:
    return get_crypto_info(symbol).get('emoji', '')

def get_exchange_symbol(crypto_symbol: str, exchange: str) -> str:
    """Get the exchange-specific symbol for a cryptocurrency."""
    crypto = get_crypto_info(crypto_symbol)
    if "symbols" in crypto and exchange in crypto["symbols"]:
        return crypto["symbols"][exchange]
    return crypto_symbol

def get_supported_exchanges() -> list:
    return list(SOURCES.keys())

def get_supported_symbols() -> list:
    return list(CRYPTO_METADATA.keys())

def get_primary_symbols() -> dict:
    """Get primary cryptocurrency symbols for all exchanges."""
    symbols = {}
    for exchange in BASE_SOURCES:
        symbols[exchange] = [
            data["symbols"].get(exchange, symbol)
            for symbol, data in CRYPTO_METADATA.items()
            if "symbols" in data and exchange in data["symbols"] and data.get("priority", 999) <= 10
        ]
    return symbols

def get_symbol_mapping() -> dict:
    """Generate symbol mapping for all exchanges."""
    mapping = {}
    for exchange in BASE_SOURCES:
        mapping[exchange] = {
            symbol: data["symbols"].get(exchange, symbol)
            for symbol, data in CRYPTO_METADATA.items()
            if "symbols" in data and exchange in data["symbols"]
        }
    return mapping

def get_symbol_config() -> dict:
    """Generate symbol configuration for display purposes."""
    return {
        symbol: {"symbol": data["symbols"].get("binance", symbol), "display": f"{data['emoji']} {symbol}"}
        for symbol, data in CRYPTO_METADATA.items()
        if "symbols" in data and "binance" in data["symbols"]
    }

# Extract conversion factors for backward compatibility
SATOSHI_TO_BTC = CRYPTO_METADATA["BTC"]["conversion_factor"]
WEI_TO_ETH = CRYPTO_METADATA["ETH"]["conversion_factor"]
LAMPORTS_TO_SOL = CRYPTO_METADATA["SOL"]["conversion_factor"]

# Generate dynamic configurations
SYMBOLS = get_primary_symbols()
SYMBOL_MAPPING = get_symbol_mapping()
SYMBOL_CONFIG = get_symbol_config()

# Extract individual symbols for backward compatibility
SYMBOL_BTC = get_exchange_symbol("BTC", "binance")
SYMBOL_ETH = get_exchange_symbol("ETH", "binance")
SYMBOL_SOL = get_exchange_symbol("SOL", "binance")
SYMBOL_LINK = get_exchange_symbol("LINK", "binance")
SYMBOL_SUI = get_exchange_symbol("SUI", "binance")
SYMBOL_BNB = get_exchange_symbol("BNB", "binance")
