# Mean Reversion Trading System

A complete mean reversion trading system for cryptocurrency perpetual futures, featuring backtesting optimization, live trading bots, and comprehensive utility functions for HyperLiquid and Binance exchanges.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [What is Mean Reversion?](#what-is-mean-reversion)
3. [How is the Moving Average Calculated?](#how-is-the-moving-average-calculated)
4. [How the System Works](#how-the-system-works)
5. [The Three Components](#the-three-components)
6. [Visual Example](#visual-example)
7. [Why Mean Reversion Works](#why-mean-reversion-works-sometimes)
8. [Key Parameters Summary](#key-parameters-summary)
9. [Quick Start](#quick-start)
10. [System Architecture](#system-architecture)
11. [File Descriptions](#file-descriptions)
12. [Strategy Logic](#strategy-logic)
13. [Configuration](#configuration)
14. [Setup & Installation](#setup--installation)
15. [Usage](#usage)
16. [Risk Management](#risk-management)
17. [Data Files](#data-files)
18. [Troubleshooting](#troubleshooting)

---

## Project Overview

This project implements a **mean reversion trading strategy** across multiple cryptocurrency perpetual futures markets. The system consists of three main components:

1. **Backtesting Engine** (`mean_reversion_backtest.py`) - Optimizes strategy parameters using historical data
2. **Live Trading Bot** (`mean_reversion_live_trading_bot.py`) - Executes trades on HyperLiquid exchange
3. **Multi-Ticker Scanner** (`mean_reversion_74_tickers_scan.py`) - Scans 74+ tickers for opportunities on Binance

The strategy is based on the statistical tendency for prices to revert to their mean (average) after significant deviations.

---

## What is Mean Reversion?

**Mean reversion** is a financial theory suggesting that asset prices and historical returns eventually return to their long-term average level. This strategy exploits temporary price extremes:

### Core Principle
```
When price deviates significantly from its moving average:
  - If price is TOO LOW  -> BUY (expect price to rise back to average)
  - If price is TOO HIGH -> SELL (expect price to fall back to average)
```

### Mathematical Formula
```python
SMA = Simple Moving Average over N periods

Buy Signal:  Current Price < SMA * (1 - buy_threshold%)
Sell Signal: Current Price > SMA * (1 + sell_threshold%)
```

### Example
If SMA(20) = $100 and buy_threshold = 15%:
- Buy when price drops below $85 (100 * 0.85)
- Sell when price rises above $115 (100 * 1.15)

---

## How is the Moving Average Calculated?

The **Simple Moving Average (SMA)** is the core of this strategy. Here's exactly how it works:

### Formula

```python
SMA = (Price₁ + Price₂ + Price₃ + ... + Priceₙ) / n
```

Where `n` is the number of periods (candles) to average.

### Calculation Example

For a **14-period SMA** on 4-hour candles:

```
Last 14 closing prices:
$95,000, $96,200, $94,800, $97,100, $96,500, $95,300, $94,900,
$96,800, $97,500, $96,100, $95,600, $97,200, $96,400, $95,800

SMA = ($95,000 + $96,200 + ... + $95,800) / 14
SMA = $1,345,200 / 14
SMA = $96,085.71
```

### In Code

The backtest uses the `backtesting.py` library's SMA indicator:

```python
from backtesting.test import SMA

class SMABuySellStrategy(Strategy):
    sma_period = 14  # Number of candles to average

    def init(self):
        # Calculate SMA of closing prices over sma_period candles
        self.sma = self.I(SMA, self.data.Close, self.sma_period)

    def next(self):
        current_sma = self.sma[-1]  # Latest SMA value
        current_price = self.data.Close[-1]  # Latest close price

        # Calculate thresholds
        buy_threshold = current_sma * (1 - self.buy_pct / 100)
        sell_threshold = current_sma * (1 + self.sell_pct / 100)
```

### Can You Calculate It Yourself?

Yes! Here's a simple Python function:

```python
def calculate_sma(prices, period):
    """
    Calculate Simple Moving Average

    Args:
        prices: List of closing prices
        period: Number of periods to average

    Returns:
        SMA value
    """
    if len(prices) < period:
        return None

    return sum(prices[-period:]) / period

# Example usage:
closing_prices = [95000, 96200, 94800, 97100, 96500, 95300, 94900,
                  96800, 97500, 96100, 95600, 97200, 96400, 95800]
sma_14 = calculate_sma(closing_prices, 14)
print(f"14-period SMA: ${sma_14:,.2f}")  # Output: $96,085.71
```

### Why SMA Period Matters

| Period | Sensitivity | Best For |
|--------|-------------|----------|
| 10 | High | Fast markets, more trades |
| 14 | Medium | Balanced approach |
| 20 | Low | Slower markets, fewer false signals |

The backtest optimizes across SMA periods 10-20 to find what works best for each asset.

---

## How the System Works

### Step 1: Calculate the "Mean" (Average Price)

The system uses a **Simple Moving Average (SMA)** - typically the average closing price over the last 14-20 candles.

```python
SMA = (Close₁ + Close₂ + ... + Close₂₀) / 20
```

### Step 2: Define "Too Far" Thresholds

The system triggers trades when price deviates by a percentage from the SMA:

```
Buy Threshold  = SMA × (1 - 15%)  = SMA × 0.85
Sell Threshold = SMA × (1 + 15%)  = SMA × 1.15
```

**Example:** If SMA = $100:
- Buy when price drops below $85
- Sell when price rises above $115

### Step 3: Execute Trades

```
Current Price < Buy Threshold  → Open LONG position
Current Price > Sell Threshold → Close position (take profit)
```

---

## The Three Components

### 1. Backtester (`mean_reversion_backtest.py`)

Finds the optimal parameters by testing thousands of combinations:

```python
# Tests these ranges:
sma_period: 10-20 candles
buy_pct:    10-25% below SMA
sell_pct:   10-25% above SMA
```

Outputs a heatmap showing which combinations made the most money historically.

### 2. Live Bot (`mean_reversion_live_trading_bot.py`)

Executes trades on HyperLiquid with optimized parameters:

```python
# BTC settings (from backtest results)
'BTC': {
    'sma_period': 15,
    'buy_range': (6, 8),     # Buy 6-8% below SMA
    'sell_range': (4, 6)     # Sell 4-6% above SMA
}
```

**Trade Flow:**
1. Fetch current price and calculate SMA
2. Check if price crossed threshold
3. If BUY signal → open position with stop-loss & take-profit
4. Run every 1 minute

### 3. Multi-Ticker Scanner (`mean_reversion_74_tickers_scan.py`)

Scans 74+ crypto pairs on Binance, adding **trend filtering**:

```python
# Only trade WITH the trend
if 4H_trend == BULLISH:
    only look for BUY setups (price below 15m SMA)

if 4H_trend == BEARISH:
    only look for SELL setups (price above 15m SMA)
```

---

## Visual Example

```
Price
  │
  │     ╭─────╮ Sell Zone (SMA + 15%)
  │    ╱       ╲
  │───●─────────●─── SMA (Moving Average)
  │    ╲       ╱
  │     ╰─────╯ Buy Zone (SMA - 15%)
  │
  └──────────────────► Time

When price enters Buy Zone  → System BUYS
When price enters Sell Zone → System SELLS/CLOSES
```

---

## Why Mean Reversion Works (Sometimes)

Mean reversion exploits **overreaction** in markets:
- Panic selling pushes price too low → bounce opportunity
- FOMO buying pushes price too high → pullback opportunity

**Best conditions:** Ranging/sideways markets with clear support/resistance

**Worst conditions:** Strong trending markets (price keeps going, never reverts)

---

## Key Parameters Summary

```python
# Position Sizing
order_usd_size = 10    # $10 per trade
leverage = 3           # 3x leverage

# Thresholds (from backtest)
sma_period = 14        # 14-candle average
buy_pct = 14           # Buy 14% below SMA
sell_pct = 18          # Sell 18% above SMA

# Risk Limits
target = 9             # Take profit at 9%
max_loss = -8          # Stop loss at 8%
```

---

## Quick Start

```bash
# 1. Find optimal parameters
.moonview_env/bin/python "mean reversion june 21/mean_reversion_backtest.py"

# 2. Update mean_reversion_live_trading_bot.py with best parameters

# 3. Run live (paper trade first!)
.moonview_env/bin/python "mean reversion june 21/mean_reversion_live_trading_bot.py"
```

---

## System Architecture

```
                    +------------------+
                    |   Historical     |
                    |   OHLCV Data     |
                    |  (CSV files)     |
                    +--------+---------+
                             |
                             v
+------------------+    +----+------+    +------------------+
|  mr_bt.py        |    | Parameter |    |  mr_bot.py       |
|  (Backtest)      +--->| Optimize  +--->|  (Live Trading)  |
|                  |    |           |    |  HyperLiquid     |
+------------------+    +-----------+    +------------------+
                                                 |
                                                 v
                                         +------+------+
                                         | nice_funcs  |
                                         | (Utilities) |
                                         +------+------+
                                                 |
                +--------------------------------+--------------------------------+
                |                                |                                |
                v                                v                                v
        +-------+-------+               +-------+-------+               +--------+-------+
        | HyperLiquid   |               | Binance       |               | Order Book     |
        | Exchange API  |               | Futures API   |               | Analysis       |
        +---------------+               +---------------+               +----------------+
```

---

## File Descriptions

### 1. `mean_reversion_backtest.py` - Backtesting & Optimization Engine

**Purpose:** Find optimal strategy parameters before live trading

**Library:** `backtesting.py` with `seaborn` heatmaps

**What it does:**
- Loads historical OHLCV data from CSV
- Tests thousands of parameter combinations
- Generates heatmaps showing profitability by parameter
- Outputs the best-performing configuration

**Optimization Parameters:**
| Parameter | Range | Description |
|-----------|-------|-------------|
| `sma_period` | 10-20 | Number of candles for SMA calculation |
| `buy_pct` | 10-25% | How far below SMA to trigger buy |
| `sell_pct` | 10-25% | How far above SMA to trigger sell |

**Strategy Class:**
```python
class SMABuySellStrategy(Strategy):
    sma_period = 14   # SMA lookback period
    buy_pct = 1.0     # % below SMA to buy
    sell_pct = 1.0    # % above SMA to sell

    def next(self):
        buy_threshold = self.sma[-1] * (1 - self.buy_pct / 100)
        sell_threshold = self.sma[-1] * (1 + self.sell_pct / 100)

        if self.data.Close[-1] < buy_threshold:
            self.buy()
        elif self.data.Close[-1] > sell_threshold:
            self.position.close()
```

---

### 2. `mean_reversion_live_trading_bot.py` - Live HyperLiquid Trading Bot

**Purpose:** Execute mean reversion trades on HyperLiquid perpetual futures

**Exchange:** HyperLiquid (Ethereum-based DEX)

**Symbols Traded:** BTC, ETH (configurable)

**Key Features:**
- **Symbol-Specific Parameters:** Each token has optimized thresholds
- **Leverage Trading:** Default 3x leverage
- **Position Management:** Checks existing positions before new trades
- **Randomized Thresholds:** Adds randomness within ranges to avoid predictability
- **Scheduled Execution:** Runs every minute via `schedule` library

**Configuration:**
```python
symbols_data = {
    'BTC': {
        'sma_period': 15,
        'buy_range': (6, 8),      # Buy 6-8% below SMA
        'sell_range': (4, 6)      # Sell 4-6% above SMA
    },
    'ETH': {
        'sma_period': 19,
        'buy_range': (5, 7),      # Buy 5-7% below SMA
        'sell_range': (4, 6)      # Sell 4-6% above SMA
    }
}
```

**Trade Execution Flow:**
```
1. Fetch OHLCV data from HyperLiquid API
2. Calculate SMA for each symbol
3. Generate random buy/sell thresholds within configured ranges
4. Compare current price to thresholds
5. If BUY signal:
   a. Check if already in position
   b. Adjust leverage
   c. Calculate position size
   d. Open order with stop-loss and take-profit
6. If SELL signal:
   Log signal (position closing handled by existing orders)
7. Sleep and repeat
```

---

### 3. `mean_reversion_74_tickers_scan.py` - Multi-Ticker Scanner

**Purpose:** Scan 74+ cryptocurrency perpetual futures for mean reversion opportunities

**Exchange:** Binance Futures (adapted from Phemex)

**Key Features:**
- **Multi-Asset Scanning:** Trades any of 74+ perpetual contracts
- **Multi-Timeframe Analysis:** Uses 5m, 15m, and 4H timeframes
- **Trend Filtering:** Only trades in direction of 4H trend
- **PnL-Based Exits:** Auto-closes at target profit or max loss
- **Kill Switch:** Emergency position closing mechanism
- **Order Cleanup:** Cancels stale orders every 30 minutes

**Strategy Logic:**
```python
# Trend Detection (4H SMA)
if bid > sma_4h:
    trend = "BULLISH"
else:
    trend = "BEARISH"

# Entry Signals (15m + 5m confirmation)
if trend == "BULLISH":
    if price < sma_15m and candle_5m.close > candle_5m.open:  # Green candle
        entry_price = sma_15m * 0.992  # Buy 0.8% below SMA
        BUY()

if trend == "BEARISH":
    if price > sma_15m and candle_5m.close < candle_5m.open:  # Red candle
        entry_price = sma_15m * 1.008  # Sell 0.8% above SMA
        SELL()
```

**Risk Parameters:**
```python
pos_size = 30       # Position size in contracts
target = 9          # Take profit at 9% gain
max_loss = -8       # Stop loss at 8% loss
leverage = 10       # 10x leverage
```

---

### 4. `general_functions.py` - Utility Functions Library

**Purpose:** Shared trading utilities for HyperLiquid exchange

**Total Lines:** ~1,200 lines of production-ready trading functions

#### Core Functions:

| Function | Description |
|----------|-------------|
| `ask_bid(symbol)` | Get current bid/ask prices from order book |
| `get_sz_px_decimals(symbol)` | Get size and price decimal precision |
| `limit_order(coin, is_buy, sz, px, reduce_only, account)` | Place limit orders |
| `adjust_leverage_usd_size(symbol, usd_size, leverage, account)` | Set leverage and calculate position size |
| `get_position(symbol, account)` | Get current position details |
| `cancel_all_orders(account)` | Cancel all open orders |
| `kill_switch(symbol, account)` | Emergency close all positions |
| `pnl_close(symbol, target, max_loss, account)` | Close position based on PnL thresholds |

#### Data Functions:

| Function | Description |
|----------|-------------|
| `get_ohlcv2(symbol, interval, lookback_days)` | Fetch OHLCV from HyperLiquid API |
| `process_data_to_df(snapshot_data)` | Convert API response to DataFrame |
| `calculate_sma(prices, window)` | Calculate Simple Moving Average |
| `calculate_atr(df, window)` | Calculate Average True Range |
| `calculate_vwap_with_symbol(symbol)` | Calculate Volume Weighted Average Price |

#### Technical Indicators:

| Function | Description |
|----------|-------------|
| `calculate_bollinger_bands(df, length, std_dev)` | Bollinger Bands with tight/wide detection |
| `calculate_linear_regression_channel(df, length)` | Linear regression channel |
| `supply_demand_zones_hl(symbol, timeframe, limit)` | Calculate support/resistance zones |
| `volume_spike(df)` | Detect abnormal volume |

#### Advanced Features:

| Function | Description |
|----------|-------------|
| `ob_data(symbol)` | Aggregate order book from Binance, Bybit, Coinbase |
| `should_we_quote_orders()` | Market condition checker (volatility filter) |
| `open_order_deluxe(symbol_info, size, account)` | Open position with SL/TP |
| `linear_regression_bollinger(df)` | Combined LRC + BB indicator |

---

## Strategy Logic

### Entry Conditions

**Long Entry (BUY):**
1. 4H SMA shows BULLISH trend (price > SMA)
2. Price is below 15m SMA (mean reversion opportunity)
3. Latest 5m candle is GREEN (confirmation)
4. Place limit buy order at SMA * (1 - threshold%)

**Short Entry (SELL):**
1. 4H SMA shows BEARISH trend (price < SMA)
2. Price is above 15m SMA (mean reversion opportunity)
3. Latest 5m candle is RED (confirmation)
4. Place limit sell order at SMA * (1 + threshold%)

### Exit Conditions

1. **Take Profit:** Position reaches target % (default: 9%)
2. **Stop Loss:** Position reaches max loss % (default: -8%)
3. **Kill Switch:** Manual emergency close
4. **Time-Based:** Stale orders cancelled after 30 minutes

### Risk Filters

- **Volatility Check:** Uses ATR and price range to avoid high-volatility periods
- **Position Limit:** Won't open new position if already in trade
- **Order Book Analysis:** Checks liquidity before large orders

---

## Configuration

### mean_reversion_live_trading_bot.py Settings
```python
order_usd_size = 10      # USD value per trade
leverage = 3             # Leverage multiplier
timeframe = '4h'         # Candle timeframe

symbols_data = {
    'BTC': {
        'sma_period': 15,
        'buy_range': (6, 8),
        'sell_range': (4, 6)
    }
}
```

### mean_reversion_74_tickers_scan.py Settings
```python
pos_size = 30            # Contract size
target = 9               # % profit target
max_loss = -8            # % max loss
leverage = 10            # Leverage
timeframe = '15m'        # Signal timeframe
limit = 97               # Candles for SMA (96 = 24hrs)
sma = 20                 # SMA period
```

---

## Setup & Installation

### 1. Prerequisites
```bash
# Python 3.8+ required
# Install dependencies
pip install ccxt pandas numpy backtesting seaborn matplotlib schedule requests eth-account hyperliquid-python-sdk pandas-ta
```

### 2. Configure Credentials
```python
# In credentials/api_secrets.py:
HYPERLIQUID_SECRET_KEY = 'your_ethereum_private_key'
BINANCE_API_KEY = 'your_binance_api_key'
BINANCE_SECRET_KEY = 'your_binance_secret_key'
```

### 3. Data Source
The backtest now connects directly to the MoonView PostgreSQL database:
```python
# Database: localhost:5432/postgres
# Schema: crypto
# Table: binance_candles
# Symbols: BTC, ETH, and 20+ others with 4H data
```

---

## Usage

### Step 1: Run Backtest
```bash
.moonview_env/bin/python "mean reversion june 21/mean_reversion_backtest.py"
```
This will:
- Test parameter combinations
- Display optimization heatmap
- Print best parameters

### Step 2: Update Bot Configuration
Take the optimized parameters from backtest and update `mean_reversion_live_trading_bot.py`:
```python
symbols_data = {
    'BTC': {
        'sma_period': OPTIMIZED_SMA,
        'buy_range': (OPTIMIZED_BUY_LOW, OPTIMIZED_BUY_HIGH),
        'sell_range': (OPTIMIZED_SELL_LOW, OPTIMIZED_SELL_HIGH)
    }
}
```

### Step 3: Run Live Bot
```bash
.moonview_env/bin/python "mean reversion june 21/mean_reversion_live_trading_bot.py"
```

### Step 4: Monitor Positions
The bot will:
- Print current prices and thresholds
- Log all trade decisions
- Show PnL for open positions

---

## Risk Management

### Built-in Safeguards

1. **Stop Loss Orders:** Every position has automatic stop-loss
2. **Take Profit Orders:** Automatic profit-taking at target
3. **Position Limits:** Won't over-leverage existing positions
4. **Kill Switch:** Emergency close function
5. **PnL Monitoring:** Continuous position health checks

### Recommended Practices

- **Start Small:** Use minimum position sizes initially
- **Paper Trade:** Test on testnet before live trading
- **Backtest First:** Always run `mean_reversion_backtest.py` with recent data
- **Monitor Constantly:** These bots require supervision
- **Set Alerts:** Configure exchange alerts for large moves

### Risk Parameters to Adjust

| Parameter | Conservative | Moderate | Aggressive |
|-----------|--------------|----------|------------|
| `leverage` | 1-2x | 3-5x | 10x+ |
| `target` | 3-5% | 5-10% | 10-20% |
| `max_loss` | -2% | -5% | -10% |
| `pos_size` | $10-50 | $50-200 | $200+ |

---

## Data Files

**Data Source:** MoonView PostgreSQL Database

| Symbol | Timeframe | Candles | Date Range |
|--------|-----------|---------|------------|
| BTC | 4H | 2,202 | Dec 2024 - Dec 2025 |
| ETH | 4H | 2,202 | Dec 2024 - Dec 2025 |

*Legacy CSV files (WIF, POPCAT) are still present but no longer used by the backtest.*

### Data Format
```csv
timestamp,open,high,low,close,volume
2024-01-01 00:00:00,1.234,1.250,1.220,1.245,1000000
```

---

## Troubleshooting

### Common Issues

**"Invalid order size"**
- Solution: Use `get_sz_px_decimals()` to get correct precision

**"Insufficient margin"**
- Solution: Reduce `pos_size` or `leverage`

**API Rate Limits**
- Solution: Exchange has `enableRateLimit: True` - this handles throttling

**Position Not Opening**
- Check: Already in position? Use `get_position()` to verify

---

## Related Projects

- `ATC Bootcamp Code 2025/` - Additional trading strategies
- `src/agents/` - AI-powered trading agents
- `src/strategies/` - Strategy implementations

---

## Disclaimer

**This software is for educational purposes only.**

- NOT financial advice
- NOT backtested for all market conditions
- Use at your own risk
- Always test with paper trading first
- Never trade with money you can't afford to lose

---

## License

Part of the Moon Dev AI Agents project.
