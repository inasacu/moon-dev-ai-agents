# Mean Reversion Trading Strategies

This folder contains mean reversion trading bots and backtesting tools for cryptocurrency markets.

## Strategy Overview

**Mean Reversion** is based on the principle that prices tend to return to their average over time. When price deviates significantly from the SMA (Simple Moving Average), we trade in the direction that brings it back to the mean.

### Core Logic
- **BUY** when price drops below `SMA * (1 - buy_threshold%)`
- **SELL** when price rises above `SMA * (1 + sell_threshold%)`
- Uses 4H trend (SMA) to filter trade direction (only long in uptrends, only short in downtrends)

---

## Files

### 1. `mr_bot.py` - HyperLiquid Mean Reversion Bot
**Exchange:** HyperLiquid
**Symbols:** WIF, POPCAT
**Timeframe:** 4H

**Features:**
- Symbol-specific SMA periods and buy/sell ranges
- Leverage support (default: 3x)
- Position checking before opening new trades
- Scheduled execution (every 1 minute)

**Configuration:**
```python
order_usd_size = 10
leverage = 3
timeframe = '4h'

symbols_data = {
    'WIF': {'sma_period': 14, 'buy_range': (14, 15), 'sell_range': (14, 22)},
    'POPCAT': {'sma_period': 14, 'buy_range': (12, 13), 'sell_range': (14, 18)}
}
```

**Run:**
```bash
.moonview_env/bin/python "mean reversion june 21/mr_bot.py"
```

---

### 2. `mr_bt.py` - Backtest Script
**Library:** backtesting.py
**Purpose:** Optimize SMA period and buy/sell percentages

**Optimization Parameters:**
- `sma_period`: 10-20
- `buy_pct`: 10-25%
- `sell_pct`: 10-25%

**Output:** Heatmap visualization + optimal parameters

**Run:**
```bash
.moonview_env/bin/python "mean reversion june 21/mr_bt.py"
```

---

### 3. `74_tickers_mean_reversion.py` - Multi-Ticker Bot (Phemex)
**Exchange:** Phemex
**Symbols:** 74+ perpetual contracts
**Timeframe:** 15m (signals), 4H (trend filter), 5m (confirmation)

**Features:**
- Random symbol selection from 74 tickers
- Multi-timeframe analysis (5m, 15m, 4H SMAs)
- PnL-based exit (target: 9%, max loss: -8%)
- Kill switch for position closing
- Order cancellation every 30 minutes

**Strategy Logic:**
1. Check 4H SMA for trend direction (BULLISH/BEARISH)
2. If BULLISH + price < 15m SMA + 5m candle green → BUY at SMA - 0.8%
3. If BEARISH + price > 15m SMA + 5m candle red → SELL at SMA + 0.8%

**Configuration:**
```python
pos_size = 30
target = 9      # % profit target
max_loss = -8   # % max loss
leverage = 10
sma = 20
```

**Requirements:**
- `phe_symbols.csv` - List of Phemex symbols
- `dontshare_config.py` - API keys

---

### 4. `nice_funcs.py` - Utility Functions
Shared trading utilities (position management, OHLCV fetching, order execution).

---

## Data Files

| File | Description |
|------|-------------|
| `POPCAT_4h_5000.csv` | POPCAT 4H OHLCV data (5000 candles) |
| `WIF_4h_50000.csv` | WIF 4H OHLCV data (50000 candles) |

---

## Setup

1. **Configure credentials:**
   ```python
   # mr_bot.py uses:
   from credentials.api_secrets import HYPERLIQUID_SECRET_KEY

   # 74_tickers uses dontshare_config.py (create with your Phemex keys)
   ```

2. **Update data paths in mr_bt.py:**
   ```python
   data_path = 'mean reversion june 21/WIF_4h_50000.csv'
   ```

3. **Run backtest first to find optimal parameters:**
   ```bash
   .moonview_env/bin/python "mean reversion june 21/mr_bt.py"
   ```

4. **Update mr_bot.py with optimized parameters, then run live:**
   ```bash
   .moonview_env/bin/python "mean reversion june 21/mr_bot.py"
   ```

---

## Risk Warning

These bots have NOT been fully backtested for all market conditions.

**DO NOT run with real money without:**
- Extensive backtesting
- Paper trading validation
- Proper position sizing
- Stop-loss implementation

---

## Related Strategies

See also:
- `ATC Bootcamp Code 2025/Bonus_algos_6ofthem/1_turtle_trending_algo/` - Trend following
- `src/strategies/` - Additional strategy implementations
