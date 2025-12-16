# ATC Bootcamp Code 2025 - Educational Foundation

This document details the Algo Trade Camp (ATC) Bootcamp materials included in this repository and their relationship to the main Moon Dev AI Agents project.

## Overview

The `ATC Bootcamp Code 2025/` folder contains a comprehensive cryptocurrency trading course that teaches algorithmic trading from scratch. This is the **educational foundation** that preceded and informed the development of the 48+ agent system in the main project.

**Location**: `/ATC Bootcamp Code 2025/`

## What's Included

### Core Learning Modules

| File | Topic | Description |
|------|-------|-------------|
| `2_coding_basics.py` | Python Fundamentals | Variables, loops, functions, data types |
| `2.1-anaconda-pip-vsc.py` | Environment Setup | Conda, pip, VSCode configuration |
| `4-algo_orders.py` | Order Placement | Limit orders, cancellation, scheduling |
| `6_sma.py` | Simple Moving Average | SMA indicator implementation with trading logic |
| `7_rsi.py` | RSI Indicator | Relative Strength Index tutorial |
| `8_vwap.py` | VWAP | Volume Weighted Average Price |
| `13_backtesting.py` | Backtesting | Backtrader framework setup |

### Risk Management (`5_risk/`)

Three files covering position sizing and risk controls:
- **5_risk.py** - PnL monitoring, kill switches, position limits
- **5_risk_mgmt_hl.py** - HyperLiquid-specific risk management
- **nice_funcs.py** - Risk-focused utility functions

Key concepts taught:
- Emergency kill switches (max loss triggers)
- Position cost monitoring
- Graceful exits using limit orders
- Target profit and stop-loss automation

### Advanced Indicators (`9_more_indicators/`)

- **9_vwma.py** - Volume Weighted Moving Average
- **pandas_ta_review.py** - pandas_ta library tutorial (130+ indicators)
- **talib_review.py** - TA-Lib examples

### Six Bonus Algorithms (`Bonus_algos_6ofthem/`)

Complete, production-ready trading strategies:

| # | Strategy | Description |
|---|----------|-------------|
| 1 | **Turtle Trending** | Classic breakout system - 55-bar highs/lows, 2x ATR stops |
| 2 | **Correlation** | ETH correlation trading on lagging altcoins |
| 3 | **Consolidation Pop** | Breakout detection from consolidation zones |
| 4 | **Nadaraya-Watson** | Statistical smoothing for trend detection |
| 5 | **Market Maker** | Liquidity provision with bid/ask spread |
| 6 | **Mean Reversion** | 74-ticker mean reversion strategy |

### HyperLiquid Bots (`HyperLiquid-Trading-Bots - Members only/`)

DEX-specific implementations:
- **arb.py** - BTC/ETH arbitrage based on funding rates
- **nice_funcs.py** - HyperLiquid utility functions
- Supply/demand zone analysis

### OpenAI Assistants (`Open-AI-Assistants for Bootcamp Members Only/`)

The **precursor to the RBI Agent** - AI-powered strategy generation:

```
User provides strategy idea
    → AI researches and designs
    → AI generates backtestable code
    → System runs backtest
    → Results stored for analysis
```

**Key Files**:
- `ai_trader.py` through `ai_trader6.py` - Evolution of AI strategy researcher
- `ai_data_guy.py` - Data analysis specialist
- `strategies/` - 13+ AI-generated strategies (VWAP, Keltner, MACD, Ichimoku, etc.)
- `bt_code/` - 12+ backtest implementations

### Historical Data (`datasets/`)

| File | Timeframe | Size |
|------|-----------|------|
| BTCUSD-1d-1000wks-data.csv | Daily | 205KB |
| BTCUSD-1h-500wks-data.csv | Hourly | 5.5MB |
| BTCUSD-6h-500wks-data.csv | 6-Hour | 930KB |

## Technologies Used

### Exchange Integration
- **CCXT** - Unified crypto exchange API (Phemex primary)
- **cbpro** - Coinbase Pro API
- **HyperLiquid SDK** - DEX integration

### Technical Analysis
- **pandas** + **pandas_ta** - Data manipulation + 130+ indicators
- **ta-lib** - Traditional TA library
- **numpy** - Numerical computing

### Backtesting
- **backtrader** - Event-driven backtesting

### AI
- **OpenAI Assistants API** - GPT-4 with threads for strategy generation

## Benefits to Moon Dev Project

### 1. Educational Foundation

The bootcamp teaches the **building blocks** that the AI agents use:
- Order execution patterns
- Risk management primitives
- Indicator calculations
- Position sizing logic

Understanding this code helps users comprehend what the AI agents are doing under the hood.

### 2. Strategy Archetypes

The 6 bonus algorithms demonstrate strategy patterns that AI agents can learn from:

| Pattern | Bootcamp Example | Agent Application |
|---------|-----------------|-------------------|
| Trend Following | Turtle Algorithm | Trading Agent long-term signals |
| Mean Reversion | Mean Reversion Algo | Sentiment Agent contrarian plays |
| Correlation | Correlation Algo | Whale Agent correlation tracking |
| Breakout | Consolidation Pop | Chart Analysis Agent patterns |

### 3. Code Reuse

**Bootcamp `nice_funcs.py`** (456 lines) is the precursor to the main project's `src/nice_funcs.py` (1,200+ lines).

Shared patterns:
- `get_ohlcv_data()` - OHLCV fetching
- `token_price()` - Price retrieval
- Position management functions
- Order book analysis

### 4. RBI Agent Origin

The `Open-AI-Assistants/` folder shows the **evolution** that became the RBI Agent:

```
Bootcamp: ai_trader.py (OpenAI Assistants API, manual thread management)
    ↓ Evolution
Main Project: rbi_agent.py (DeepSeek-R1, ModelFactory, automated backtesting)
```

### 5. Backtesting Datasets

The historical data can be used with the main project's backtesting capabilities:
- Same CSV format as `src/data/rbi/BTC-USD-15m.csv`
- Additional timeframes (daily, 6-hour)
- Longer history (up to 1000 weeks)

## Integration Opportunities

### Using Bootcamp Strategies with Main Project

1. **Port Bonus Algorithms to Strategy Format**:
```python
# In src/strategies/turtle_strategy.py
from src.strategies.base_strategy import BaseStrategy

class TurtleStrategy(BaseStrategy):
    name = "turtle_trending"
    description = "55-bar breakout system with 2x ATR stops"

    def generate_signals(self, token_address, market_data):
        # Port logic from Bonus_algos_6ofthem/1_turtle_trending_algo/
        ...
```

2. **Use Bootcamp Datasets for Extended Backtesting**:
```python
# Access longer historical data
bootcamp_data = "/ATC Bootcamp Code 2025/datasets/BTCUSD-1h-500wks-data.csv"
```

3. **Reference for Custom Indicator Development**:
The `9_more_indicators/` folder provides clean examples for adding custom indicators to agents.

## Key Differences: Bootcamp vs Main Project

| Aspect | Bootcamp | Main Project |
|--------|----------|--------------|
| Focus | Manual strategy coding | AI agent orchestration |
| Exchange | Phemex (CEX) | Solana DEX (BirdEye) |
| AI Usage | Optional (OpenAI Assistants) | Core (48+ agents, multi-LLM) |
| Scale | Single strategy at a time | Multi-agent parallel execution |
| Purpose | Education | Production trading system |

## Recommended Learning Path

1. **Start with Bootcamp Basics**:
   - `2_coding_basics.py` → Python fundamentals
   - `4-algo_orders.py` → Order mechanics
   - `6_sma.py` / `7_rsi.py` → Indicator logic

2. **Understand Risk Management**:
   - `5_risk/5_risk.py` → Kill switches, position sizing

3. **Study Complete Strategies**:
   - `Bonus_algos_6ofthem/1_turtle_trending_algo/` → Full system

4. **See AI Evolution**:
   - `Open-AI-Assistants/ai_trader.py` → Early AI integration

5. **Graduate to Main Project**:
   - `src/agents/rbi_agent.py` → Modern RBI system
   - `src/main.py` → Multi-agent orchestration

## Resources

- **Video Documentation**: [ATC Bootcamp Playlist](https://www.youtube.com/playlist?list=PLXrNVMjRZUJg4M4uz52iGd1LhXXGVbIFz)
- **Book Resources**: See `book_resources.txt` for recommended reading
- **Historical Data Sources**: See `historical-data-source.py` for data access instructions

## Summary

The ATC Bootcamp code is the **educational genealogy** of the Moon Dev AI Agents project. It provides:

- **Learning foundation** for understanding agent internals
- **Strategy templates** that can be ported to the agent system
- **Historical data** for extended backtesting
- **Code patterns** reused throughout the main project
- **Evolution history** showing how manual trading → AI-powered agents

For anyone looking to deeply understand the Moon Dev system, studying the bootcamp materials provides crucial context for how and why the agents work the way they do.
