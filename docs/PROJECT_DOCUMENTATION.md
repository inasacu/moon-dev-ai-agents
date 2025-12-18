# Moon Dev AI Agents - Project Documentation

**Last Updated:** 2025-12-18
**Version:** 1.0.0
**Migration Target:** MoonView (`~/WorkLocal/moonview/`)

This document provides comprehensive documentation for the Moon Dev AI Agents project. It is designed to help AI agents and developers understand the project structure, available resources, and how components will migrate to MoonView.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Core Source Code](#core-source-code)
4. [Agents System](#agents-system)
5. [Models (LLM Abstraction)](#models-llm-abstraction)
6. [Trading Utilities](#trading-utilities)
7. [Configuration](#configuration)
8. [Shared Resources](#shared-resources)
9. [ATC Bootcamp Materials](#atc-bootcamp-materials)
10. [Migration Mapping](#migration-mapping)

---

## Project Overview

Moon Dev AI Agents is an experimental AI trading system that orchestrates 48+ specialized AI agents to analyze markets, execute strategies, and manage risk across cryptocurrency markets (primarily Solana and HyperLiquid).

### Core Capabilities

| Feature | Description |
|---------|-------------|
| Multi-Agent System | 58 AI agents for trading, analysis, research, content |
| LLM Abstraction | Unified interface for 10 LLM providers |
| Multi-Exchange | Solana (Jupiter), HyperLiquid, Aster, X10 |
| RBI System | Research-Backtest-Implement for AI strategy generation |
| Training Materials | ATC Bootcamp Code 2025 |

### Project Statistics

| Category | Count |
|----------|-------|
| Agent files | 58 |
| Model providers | 10 |
| Utility files (nice_funcs*) | 4 |
| Total source lines | ~42,000 |
| ATC Bootcamp files | 73 |

---

## Directory Structure

```
moon-dev-ai-agents/
├── src/                           # Main source code
│   ├── agents/                    # 58 AI agents
│   ├── models/                    # LLM abstraction layer (10 providers)
│   ├── strategies/                # Trading strategy templates
│   ├── scripts/                   # Utility scripts
│   ├── data/                      # Agent outputs & RBI results
│   ├── config.py                  # Main configuration
│   ├── main.py                    # Orchestrator
│   ├── nice_funcs.py              # Solana trading utilities
│   ├── nice_funcs_hyperliquid.py  # HyperLiquid utilities
│   ├── nice_funcs_extended.py     # X10 exchange utilities
│   ├── nice_funcs_aster.py        # Aster exchange utilities
│   ├── exchange_manager.py        # Multi-exchange manager
│   └── ezbot.py                   # Legacy trading controller
│
├── config/                        # Shared config (symlinked from moonview)
├── credentials/                   # API keys (symlinked from moonview)
├── data/                          # Shared data folder
├── docs/                          # Documentation
├── logs/                          # Application logs
│
├── ATC Bootcamp Code 2025/        # Training materials (73 Python files)
│   ├── 10_day10_bots/            # Day 10 bots
│   ├── 11_day11_bots/            # Day 11 bots
│   ├── 12_day12_bots/            # Day 12 bots
│   ├── Bonus_algos_6ofthem/      # 6 bonus algorithms
│   ├── HyperLiquid-Trading-Bots/ # HyperLiquid bots
│   ├── Open-AI-Assistants/       # RBI system source
│   └── datasets/                  # Training data
│
├── 2025 Data Sources/             # Data fetching scripts
├── mean reversion june 21/        # Mean reversion strategy project
│
├── .moonview_env -> ~/WorkLocal/moonview/.moonview_env  # Shared Python env
├── CLAUDE.md                      # AI agent instructions
└── requirements.txt               # Python dependencies
```

---

## Core Source Code

### Root Files (`src/`)

| File | Lines | Purpose | MoonView Target |
|------|-------|---------|-----------------|
| `config.py` | ~100 | Trading configuration | `config/modules/trading.py` |
| `main.py` | ~200 | Agent orchestrator | `agents/orchestrator.py` |
| `nice_funcs.py` | 1,183 | Solana trading utilities | Decompose to `moonview.trading.*` |
| `nice_funcs_hyperliquid.py` | 924 | HyperLiquid utilities | `moonview.api.exchanges.hyperliquid` |
| `nice_funcs_extended.py` | 851 | X10 exchange utilities | `moonview.api.exchanges.x10` |
| `nice_funcs_aster.py` | 837 | Aster exchange utilities | `moonview.api.exchanges.aster` |
| `exchange_manager.py` | 381 | Multi-exchange manager | `moonview.api.exchanges` |
| `ezbot.py` | 261 | Legacy trading controller | Evaluate |

### Key Functions in `nice_funcs.py`

| Function | Purpose | MoonView Location |
|----------|---------|-------------------|
| `token_overview(address)` | Get token metadata | `moonview.api.blockchain.solana` |
| `token_price(address)` | Get current price | `moonview.api.blockchain.solana` |
| `token_security_info(address)` | Security check | `moonview.api.blockchain.solana` |
| `market_buy(token, amount, slippage)` | Execute buy | `moonview.trading.orders` |
| `market_sell(token, amount, slippage)` | Execute sell | `moonview.trading.orders` |
| `get_position(token)` | Get position info | `moonview.trading.positions` |
| `pnl_close(token)` | Close with P&L check | `moonview.trading.risk` |
| `chunk_kill(token, max_size, slippage)` | Gradual close | `moonview.trading.orders` |
| `get_data(address, days, timeframe)` | Get OHLCV data | `moonview.data.database` |
| `supply_demand_zones(token, tf, limit)` | S/D analysis | `moonview.trading.signals` |

### Key Functions in `nice_funcs_hyperliquid.py`

| Function | Purpose | MoonView Location |
|----------|---------|-------------------|
| `ask_bid(symbol)` | Get order book | `moonview.api.exchanges.hyperliquid` |
| `get_position(symbol, account)` | Position info | `moonview.trading.positions` |
| `set_leverage(symbol, leverage, account)` | Set leverage | `moonview.trading.leverage` |
| `limit_order(coin, is_buy, sz, px, reduce_only, account)` | Limit order | `moonview.trading.orders` |
| `market_buy/sell(symbol, usd_size, account)` | Market orders | `moonview.trading.orders` |
| `kill_switch(symbol, account)` | Emergency close | `moonview.trading.risk` |
| `pnl_close(symbol, target, max_loss, account)` | P&L close | `moonview.trading.risk` |
| `get_data(symbol, timeframe, bars, add_indicators)` | OHLCV + TA | `moonview.data.database` |
| `add_technical_indicators(df)` | Add TA indicators | `moonview.trading.indicators` |

---

## Agents System

### Location: `src/agents/`

58 AI agents organized by function.

### Agent Categories

#### Trading Agents (4)
| Agent | Lines | Purpose | Priority |
|-------|-------|---------|----------|
| `trading_agent.py` | 1,195 | Trade execution | Critical |
| `risk_agent.py` | 631 | Risk management | Critical |
| `strategy_agent.py` | 305 | Strategy selection | Critical |
| `copybot_agent.py` | 326 | Copy trading | High |

#### Analysis Agents (7)
| Agent | Lines | Purpose | Priority |
|-------|-------|---------|----------|
| `sentiment_agent.py` | 516 | Market sentiment | High |
| `whale_agent.py` | 679 | Whale activity | High |
| `funding_agent.py` | 527 | Funding rates | High |
| `funding_agent_2.py` | 310 | Enhanced funding | Merge |
| `liquidation_agent.py` | 588 | Liquidation tracking | High |
| `chartanalysis_agent.py` | 446 | Technical analysis | High |
| `volume_agent.py` | 734 | Volume analysis | Medium |

#### Research Agents (7)
| Agent | Lines | Purpose | Priority |
|-------|-------|---------|----------|
| `rbi_agent.py` | 1,049 | AI strategy generation | High |
| `research_agent.py` | 569 | Web research | High |
| `backtest_runner.py` | ~200 | Backtest execution | High |
| `rbi_agent_pp.py` | 1,313 | Superseded | Skip |
| `rbi_agent_pp_multi.py` | 1,838 | Superseded | Skip |
| `rbi_agent_v2.py` | 874 | Superseded | Skip |
| `rbi_agent_v3.py` | 1,167 | Evaluate | Maybe |

#### Content Agents (5)
| Agent | Lines | Purpose | Priority |
|-------|-------|---------|----------|
| `chat_agent.py` | 653 | Interactive chat | Medium |
| `clips_agent.py` | 668 | Video clips | Medium |
| `tweet_agent.py` | 270 | Twitter content | Medium |
| `video_agent.py` | 484 | Video generation | Medium |
| `prompt_agent.py` | 510 | Prompt engineering | Medium |

#### Data Agents (7)
| Agent | Lines | Purpose | Priority |
|-------|-------|---------|----------|
| `coingecko_agent.py` | 749 | CoinGecko data | Medium |
| `polymarket_agent.py` | 1,485 | Prediction markets | Medium |
| `polymarket_websearch_agent.py` | 1,440 | Enhanced polymarket | Medium |
| `scraper_agent.py` | 685 | Web scraping | Medium |
| `websearch_agent.py` | 1,280 | Web search | Medium |
| `focus_agent.py` | 542 | Focus tracking | Low |
| `new_or_top_agent.py` | 543 | Token discovery | Medium |

#### Specialized Agents (9)
| Agent | Lines | Purpose | Priority |
|-------|-------|---------|----------|
| `sniper_agent.py` | 337 | Token sniping | Low |
| `solana_agent.py` | 364 | Solana-specific | Medium |
| `million_agent.py` | ~300 | Large trades | Low |
| `tx_agent.py` | 273 | Transaction analysis | Low |
| `compliance_agent.py` | 503 | Compliance | Low |
| `giveaway_agent.py` | 339 | Giveaways | Low |
| `housecoin_agent.py` | 615 | Specific token | Low |
| `listingarb_agent.py` | 762 | Listing arbitrage | Medium |
| `fundingarb_agent.py` | 354 | Funding arbitrage | Medium |

#### Deprecated/Experimental (19)
| Agent | Lines | Reason |
|-------|-------|--------|
| `chat_agent_ad.py` | 1,018 | Old version |
| `chat_agent_og.py` | 1,111 | Old version |
| `chat_question_generator.py` | 228 | Utility |
| `clean_ideas.py` | 280 | Utility script |
| `code_runner_agent.py` | 941 | Security risk |
| `demo_countdown.py` | ~100 | Demo only |
| `example_unified_agent.py` | 217 | Template |
| `phone_agent.py` | 797 | Hardware-specific |
| `rbi_agent_v2_simple.py` | 313 | Superseded |
| `rbi_batch_backtester.py` | 316 | Merge into runner |
| `realtime_clips_agent.py` | 875 | Merge into clips |
| `shortvid_agent.py` | 287 | Merge into video |
| `stream_agent.py` | 289 | Unclear purpose |
| `swarm_agent.py` | 571 | Experimental |
| `tiktok_agent.py` | 1,288 | Platform-specific |

### Shared Agent Infrastructure

#### `api.py` - MoonDevAPI Class (588 lines)
| Method | Purpose | MoonView Location |
|--------|---------|-------------------|
| `get_liquidation_data(limit)` | Liquidation data | `moonview.api.moondev` |
| `get_funding_data()` | Funding rates | `moonview.api.moondev` |
| `get_oi_total()` | Open interest | `moonview.api.moondev` |
| `get_oi_data()` | Detailed OI | `moonview.api.moondev` |
| `get_copybot_follow_list()` | Copybot wallets | `moonview.api.moondev` |
| `get_whale_addresses()` | Whale wallets | `moonview.api.moondev` |

#### `base_agent.py` - Foundation Class
Base class for agent development pattern.

---

## Models (LLM Abstraction)

### Location: `src/models/`

Unified interface for 10 LLM providers.

### Files

| File | Lines | Purpose | MoonView Target |
|------|-------|---------|-----------------|
| `__init__.py` | ~30 | Exports | `models/__init__.py` |
| `model_factory.py` | ~150 | Factory pattern | `models/model_factory.py` |
| `base_model.py` | ~100 | Abstract base | `models/base_model.py` |
| `claude_model.py` | ~120 | Anthropic Claude | `models/providers/claude.py` |
| `openai_model.py` | 440 | OpenAI GPT | `models/providers/openai.py` |
| `deepseek_model.py` | ~100 | DeepSeek | `models/providers/deepseek.py` |
| `groq_model.py` | ~100 | Groq (fast) | `models/providers/groq.py` |
| `gemini_model.py` | ~100 | Google Gemini | `models/providers/gemini.py` |
| `ollama_model.py` | ~100 | Local Ollama | `models/providers/ollama.py` |
| `openrouter_model.py` | ~100 | OpenRouter | `models/providers/openrouter.py` |
| `xai_model.py` | ~80 | xAI Grok | `models/providers/xai.py` |
| `token_tracker.py` | ~200 | Usage tracking | `models/utils/token_tracker.py` |

### Usage Pattern

```python
from src.models.model_factory import ModelFactory

# Create model
model = ModelFactory.create_model('anthropic')  # or 'openai', 'deepseek', etc.

# Generate response
response = model.generate_response(
    system_prompt="You are a helpful assistant.",
    user_content="Analyze BTC price action.",
    temperature=0.7,
    max_tokens=1000
)
```

---

## Trading Utilities

### Utility Files Comparison

| File | Lines | Exchange | Key Functions |
|------|-------|----------|---------------|
| `nice_funcs.py` | 1,183 | Solana/Jupiter | token_overview, market_buy/sell, get_position |
| `nice_funcs_hyperliquid.py` | 924 | HyperLiquid | ask_bid, limit_order, get_data, add_indicators |
| `nice_funcs_extended.py` | 851 | X10 | ExtendedExchangeAPI class |
| `nice_funcs_aster.py` | 837 | Aster | Similar pattern to extended |

### Duplicated Functions Across Files

| Function | Files | Canonical Location |
|----------|-------|-------------------|
| `market_buy()` | 4 files | `moonview.trading.orders` |
| `market_sell()` | 4 files | `moonview.trading.orders` |
| `get_position()` | 4 files | `moonview.trading.positions` |
| `close_position()` | 4 files | `moonview.trading.positions` |
| `chunk_kill()` | 3 files | `moonview.trading.orders` |
| `pnl_close()` | 3 files | `moonview.trading.risk` |
| `cancel_all_orders()` | 4 files | `moonview.trading.orders` |
| `limit_order()` | 3 files | `moonview.trading.orders` |
| `ask_bid()` | 2 files | `moonview.trading.market_data` |
| `get_data()` | 3 files | `moonview.data.database` |
| `add_technical_indicators()` | 2 files | `moonview.trading.indicators` |

---

## Configuration

### `src/config.py` Settings

#### Exchange Configuration
```python
EXCHANGE = 'solana'  # Options: 'solana', 'hyperliquid'
HYPERLIQUID_SYMBOLS = ['BTC', 'ETH', 'SOL']
HYPERLIQUID_LEVERAGE = 5
```

#### Token Management
```python
USDC_ADDRESS = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
SOL_ADDRESS = "So11111111111111111111111111111111111111111"
EXCLUDED_TOKENS = [USDC_ADDRESS, SOL_ADDRESS]
MONITORED_TOKENS = [...]
```

#### Risk Management
```python
CASH_PERCENTAGE = 20        # Min % in USDC
MAX_POSITION_PERCENTAGE = 30  # Max % per position
MAX_LOSS_USD = 25
MAX_GAIN_USD = 25
MINIMUM_BALANCE_USD = 50
USE_AI_CONFIRMATION = True
```

#### AI Settings
```python
AI_MODEL = "claude-3-haiku-20240307"
AI_MAX_TOKENS = 1024
AI_TEMPERATURE = 0.7
```

#### Agent Settings
```python
SLEEP_BETWEEN_RUNS_MINUTES = 15
ENABLE_STRATEGIES = True
STRATEGY_MIN_CONFIDENCE = 0.7
```

---

## Shared Resources

### Already Unified with MoonView

| Resource | Mechanism | Path |
|----------|-----------|------|
| Python Environment | Symlink | `.moonview_env` → `~/WorkLocal/moonview/.moonview_env` |
| API Credentials | Symlink | `credentials/` → shared |
| Config Module | Symlink | `config/` → shared |
| Data Folder | Synced | `data/` structure |

### Credentials Module

```python
from credentials.api_secrets import (
    ANTHROPIC_KEY,
    OPENAI_KEY,
    DEEPSEEK_KEY,
    GROQ_API_KEY,
    GEMINI_KEY,
    BINANCE_API_KEY,
    HYPERLIQUID_KEY,
    BIRDEYE_API_KEY,
    MOONDEV_API_KEY,
)
```

---

## ATC Bootcamp Materials

### Location: `ATC Bootcamp Code 2025/`

73 Python files for educational purposes.

### Structure

```
ATC Bootcamp Code 2025/
├── 2_coding_basics.py          # Day 2
├── 4-algo_orders.py            # Day 4
├── 5_risk/                     # Day 5 - Risk management
├── 6_sma.py                    # Day 6 - SMA indicator
├── 7_rsi.py                    # Day 7 - RSI indicator
├── 8_vwap.py                   # Day 8 - VWAP indicator
├── 9_more_indicators/          # Day 9 - More indicators
├── 10_day10_bots/              # Day 10 - First bot
├── 11_day11_bots/              # Day 11 - Second bot
├── 12_day12_bots/              # Day 12 - Third bot
├── 13_backtesting.py           # Day 13 - Backtesting
├── Bonus_algos_6ofthem/        # 6 bonus algorithms
│   ├── 1_turtle_trending_algo/
│   ├── 2_correlation_algo/
│   ├── 3_consolidation_pop_algo/
│   ├── 4_nadarya_watson_algo/
│   ├── 5_market_maker/
│   └── 6_mean_reversion/
├── HyperLiquid-Trading-Bots/   # HyperLiquid bots
├── Open-AI-Assistants/         # RBI system source (Days 14-15)
├── datasets/                   # Training data
└── day 2 projects/             # Day 2 projects
```

### Migration Status

| Component | Status | Notes |
|-----------|--------|-------|
| Bootcamp Code | Keep Here | Training materials |
| Bonus Algorithms | Evaluate | May port strategies to moonview |
| RBI System | Migrate | Core of rbi_agent.py |

---

## Migration Mapping

### Overview

| Source (moon-dev-ai-agents) | Target (MoonView) | Status |
|-----------------------------|-------------------|--------|
| `src/models/` | `models/` or `src/moonview/models/` | To migrate |
| `src/agents/` (38 core) | `agents/` | To migrate |
| `src/agents/` (20 deprecated) | N/A | Skip |
| `src/nice_funcs.py` | Decompose to `moonview.*` | To decompose |
| `src/nice_funcs_hyperliquid.py` | `moonview.api.exchanges.hyperliquid` | To merge |
| `src/config.py` | `config/modules/` | To merge |
| `ATC Bootcamp Code 2025/` | Keep here | Training only |

### Function Migration Map

| Function | Source File | MoonView Target | Already Exists? |
|----------|-------------|-----------------|-----------------|
| `token_overview()` | nice_funcs.py | moonview.api.blockchain.solana | No |
| `token_price()` | nice_funcs.py | moonview.api.blockchain.solana | No |
| `market_buy()` | nice_funcs*.py | moonview.trading.orders | Partial |
| `market_sell()` | nice_funcs*.py | moonview.trading.orders | Partial |
| `get_position()` | nice_funcs*.py | moonview.trading.positions | Yes |
| `pnl_close()` | nice_funcs*.py | moonview.trading.risk | Yes |
| `ask_bid()` | nice_funcs_hl.py | moonview.trading.market_data | Yes |
| `get_data()` | nice_funcs*.py | moonview.data.database | Yes |
| `add_technical_indicators()` | nice_funcs_hl.py | moonview.trading.indicators | Yes |
| `calculate_rsi()` | Various | moonview.trading.indicators.momentum | Yes |
| `calculate_sma()` | Various | moonview.trading.indicators.trend | Yes |
| `MoonDevAPI` | agents/api.py | moonview.api.moondev | Partial |

### Class Migration Map

| Class | Source File | MoonView Target | Exists in MoonView? |
|-------|-------------|-----------------|---------------------|
| `ModelFactory` | models/model_factory.py | models/model_factory.py | No - Migrate |
| `BaseModel` | models/base_model.py | models/base_model.py | No - Migrate |
| `ClaudeModel` | models/claude_model.py | models/providers/claude.py | No - Migrate |
| `OpenAIModel` | models/openai_model.py | models/providers/openai.py | No - Migrate |
| `MoonDevAPI` | agents/api.py | moonview.api.moondev | Partial - Merge |
| `ExtendedExchangeAPI` | nice_funcs_extended.py | moonview.api.exchanges.x10 | No - Migrate |
| `TokenTracker` | models/token_tracker.py | models/utils/token_tracker.py | No - Migrate |

---

## Quick Reference

### Common Imports (Current)

```python
# Models
from src.models.model_factory import ModelFactory
from src.models import ClaudeModel, OpenAIModel

# Agents
from src.agents.api import MoonDevAPI
from src.agents.risk_agent import RiskAgent

# Trading
from src.nice_funcs import token_overview, market_buy, get_position
from src.nice_funcs_hyperliquid import ask_bid, limit_order, get_data

# Config
from src.config import AI_MODEL, MONITORED_TOKENS, MAX_LOSS_USD

# Credentials
from credentials.api_secrets import ANTHROPIC_KEY, BINANCE_API_KEY
```

### Common Imports (After Migration to MoonView)

```python
# Models
from models import ModelFactory
from models.providers import ClaudeModel, OpenAIModel

# Agents
from agents.api import MoonDevAPI
from agents.trading.risk_agent import RiskAgent

# Trading
from moonview.api.blockchain.solana import token_overview
from moonview.trading.orders import market_buy
from moonview.trading.positions import get_position
from moonview.trading.market_data import ask_bid
from moonview.data.database import get_data

# Config
from config import CRYPTO_METADATA, AI_SETTINGS

# Credentials
from credentials.api_secrets import ANTHROPIC_KEY, BINANCE_API_KEY
```

---

## Related Documentation

- `PROJECT_STRUCTURE.md` - Detailed file inventory and duplication report
- `MOONVIEW_TRANSITION.md` - Migration guide overview
- `CLAUDE.md` - AI agent instructions
- `~/WorkLocal/moonview/docs/MIGRATION_PLAN.md` - Master migration plan
