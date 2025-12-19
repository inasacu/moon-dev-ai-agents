# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## MIGRATION NOTICE

**This project has been migrated to MoonView.**

| Item | Status |
|------|--------|
| **Active Development** | `~/WorkLocal/moonview/` |
| **This Repository** | Reference & Upstream Sync Only |
| **Agents** | Migrated to `moonview/agents/` (38 agents) |
| **Models** | Migrated to `moonview/models/` (10 providers) |

### For Active Development, Use MoonView:
```bash
cd ~/WorkLocal/moonview
source .moonview_env/bin/activate
python -m agents.orchestrator --list
```

### This Repository Is Now:
1. **Upstream Sync Target** - Auto-merges Moon Dev updates via `sync_upstream_daily.sh`
2. **Reference Codebase** - Original Moon Dev implementations
3. **Training Materials** - ATC Bootcamp Code 2025

See `docs/MOONVIEW_TRANSITION.md` for full migration details.

---

## Project Overview

This is an experimental AI trading system that orchestrates 48+ specialized AI agents to analyze markets, execute strategies, and manage risk across cryptocurrency markets (primarily Solana). The project uses a modular agent architecture with unified LLM provider abstraction supporting Claude, GPT-4, DeepSeek, Groq, Gemini, and local Ollama models.

## Key Development Commands

### Environment Setup
```bash
# This project shares a Python venv with ~/WorkLocal/moonview
# The .moonview_env symlink points to the shared environment

# Activate the shared environment
source .moonview_env/bin/activate

# Or use the Python directly
.moonview_env/bin/python src/main.py

# Install/update dependencies (updates shared environment)
.moonview_env/bin/pip install -r requirements.txt

# IMPORTANT: Update requirements.txt every time you add a new package
.moonview_env/bin/pip freeze > requirements.txt
```

#### Shared Environment Details
- **Location**: Symlink `.moonview_env` → `~/WorkLocal/moonview/.moonview_env`
- **Python Version**: 3.13.3
- **Key Packages**: anthropic, solana, groq, google-generativeai, discord.py, tweepy, web3, anchorpy, flask, opencv-python, and 200+ more
- **Why Shared**: Avoids redundant installs across moon-dev-ai-agents and moonview projects

### Running the System
```bash
# Run main orchestrator (controls multiple agents)
python src/main.py

# Run individual agents standalone
python src/agents/trading_agent.py
python src/agents/risk_agent.py
python src/agents/rbi_agent.py
python src/agents/chat_agent.py
# ... any agent in src/agents/ can run independently
```

### Backtesting
```bash
# Use backtesting.py library with pandas_ta or talib for indicators
# Sample OHLCV data available at:
# /Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv
```

## Architecture Overview

### Core Structure
```
src/
├── agents/              # 48+ specialized AI agents (each <800 lines)
├── models/              # LLM provider abstraction (ModelFactory pattern)
├── strategies/          # User-defined trading strategies
├── scripts/             # Standalone utility scripts
├── data/                # Agent outputs, memory, analysis results
├── config.py            # Global configuration (positions, risk limits, API settings)
├── main.py              # Main orchestrator for multi-agent loop
├── nice_funcs.py        # ~1,200 lines of shared trading utilities
├── nice_funcs_hl.py     # Hyperliquid-specific utilities
└── ezbot.py             # Legacy trading controller
```

### Agent Ecosystem

**Trading Agents**: `trading_agent`, `strategy_agent`, `risk_agent`, `copybot_agent`
**Market Analysis**: `sentiment_agent`, `whale_agent`, `funding_agent`, `liquidation_agent`, `chartanalysis_agent`
**Content Creation**: `chat_agent`, `clips_agent`, `tweet_agent`, `video_agent`, `phone_agent`
**Strategy Development**: `rbi_agent` (Research-Based Inference - codes backtests from videos/PDFs), `research_agent`
**Specialized**: `sniper_agent`, `solana_agent`, `tx_agent`, `million_agent`, `tiktok_agent`, `compliance_agent`

Each agent can run independently or as part of the main orchestrator loop.

### LLM Integration (Model Factory)

Located at `src/models/model_factory.py` and `src/models/README.md`

**Unified Interface**: All agents use `ModelFactory.create_model()` for consistent LLM access
**Supported Providers**: Anthropic Claude (default), OpenAI, DeepSeek, Groq, Google Gemini, Ollama (local)
**Key Pattern**:
```python
from src.models.model_factory import ModelFactory

model = ModelFactory.create_model('anthropic')  # or 'openai', 'deepseek', 'groq', etc.
response = model.generate_response(system_prompt, user_content, temperature, max_tokens)
```

### Configuration Management

**Primary Config**: `src/config.py`
- Trading settings: `MONITORED_TOKENS`, `EXCLUDED_TOKENS`, position sizing (`usd_size`, `max_usd_order_size`)
- Risk management: `CASH_PERCENTAGE`, `MAX_POSITION_PERCENTAGE`, `MAX_LOSS_USD`, `MAX_GAIN_USD`, `MINIMUM_BALANCE_USD`
- Agent behavior: `SLEEP_BETWEEN_RUNS_MINUTES`, `ACTIVE_AGENTS` dict in `main.py`
- AI settings: `AI_MODEL`, `AI_MAX_TOKENS`, `AI_TEMPERATURE`

**Environment Variables**: `.env` (see `.env_example` for full documentation)

| Category | Variables | Purpose |
|----------|-----------|---------|
| **Trading Data** | `BIRDEYE_API_KEY`, `MOONDEV_API_KEY`, `COINGECKO_API_KEY` | Token data, prices, signals |
| **AI Services** | `ANTHROPIC_KEY`, `OPENAI_KEY`, `DEEPSEEK_KEY`, `GROQ_API_KEY`, `GEMINI_KEY` | LLM providers |
| **Blockchain** | `SOLANA_PRIVATE_KEY`, `RPC_ENDPOINT` | Solana wallet & RPC |
| **Exchanges** | `HYPER_LIQUID_KEY`, `HYPER_LIQUID_ETH_PRIVATE_KEY`, `ASTER_API_KEY`, `X10_API_KEY` | CEX/DEX trading |
| **Social** | `TWITTER_*`, `TWILIO_*`, `YOUTUBE_API_KEY` | Content & notifications |

Setup: `cp .env_example .env` then fill in your keys

**Credentials Module** (Alternative to .env): `credentials/api_secrets.py`
- Shared with moonview project - contains all API keys in Python format
- Git-ignored and permission-protected (chmod 600)
- Usage:
```python
from credentials.api_secrets import ANTHROPIC_KEY, BINANCE_API_KEY
# Or load all to environment:
from credentials.api_secrets import load_to_env
load_to_env()
```

**Config Module**: `config/__init__.py`
- Shared configuration from moonview project (1100+ lines)
- Contains: crypto metadata, API endpoints, exchange configs, timeframes, display settings
- Usage:
```python
from config import CRYPTO_METADATA, BINANCE_API_URL, Colors, PROJECT_PATH
from config import get_exchange_symbol, get_size_indicator, format_number
```

### Shared Utilities

**`src/nice_funcs.py`** (~1,200 lines): Core trading functions
- Data: `token_overview()`, `token_price()`, `get_position()`, `get_ohlcv_data()`
- Trading: `market_buy()`, `market_sell()`, `chunk_kill()`, `open_position()`
- Analysis: Technical indicators, PnL calculations, rug pull detection

**`src/agents/api.py`**: `MoonDevAPI` class for custom Moon Dev API endpoints
- `get_liquidation_data()`, `get_funding_data()`, `get_oi_data()`, `get_copybot_follow_list()`

### Data Flow Pattern

```
Config/Input → Agent Init → API Data Fetch → Data Parsing →
LLM Analysis (via ModelFactory) → Decision Output →
Result Storage (CSV/JSON in src/data/) → Optional Trade Execution
```

## Development Rules

### File Management
- **Keep files under 800 lines** - if longer, split into new files and update README
- **DO NOT move files without asking** - you can create new files but no moving
- **Use shared environment** - `.moonview_env/bin/python` (symlinked from moonview project)
- **Update requirements.txt** after adding any new package

### Backtesting
- Use `backtesting.py` library (NOT their built-in indicators)
- Use `pandas_ta` or `talib` for technical indicators instead
- Sample data available at `/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv`

### Code Style
- **No fake/synthetic data** - always use real data or fail the script
- **Minimal error handling** - user wants to see errors, not over-engineered try/except blocks
- **No API key exposure** - never show keys from `.env` in output

### Agent Development Pattern

When creating new agents:
1. Inherit from base patterns in existing agents
2. Use `ModelFactory` for LLM access
3. Store outputs in `src/data/[agent_name]/`
4. Make agent independently executable (standalone script)
5. Add configuration to `config.py` if needed
6. Follow naming: `[purpose]_agent.py`

### Testing Strategies

Place strategy definitions in `src/strategies/` folder:
```python
class YourStrategy(BaseStrategy):
    name = "strategy_name"
    description = "what it does"

    def generate_signals(self, token_address, market_data):
        return {
            "action": "BUY"|"SELL"|"NOTHING",
            "confidence": 0-100,
            "reasoning": "explanation"
        }
```

## Important Context

### Risk-First Philosophy
- Risk Agent runs first in main loop before any trading decisions
- Configurable circuit breakers (`MAX_LOSS_USD`, `MINIMUM_BALANCE_USD`)
- AI confirmation for position-closing decisions (configurable via `USE_AI_CONFIRMATION`)

### Data Sources
1. **BirdEye API** - Solana token data (price, volume, liquidity, OHLCV)
2. **Moon Dev API** - Custom signals (liquidations, funding rates, OI, copybot data)
3. **CoinGecko API** - 15,000+ token metadata, market caps, sentiment
4. **Helius RPC** - Solana blockchain interaction

### Autonomous Execution
- Main loop runs every 15 minutes by default (`SLEEP_BETWEEN_RUNS_MINUTES`)
- Agents handle errors gracefully and continue execution
- Keyboard interrupt for graceful shutdown
- All agents log to console with color-coded output (termcolor)

### AI-Driven Strategy Generation (RBI Agent)
1. User provides: YouTube video URL / PDF / trading idea text
2. DeepSeek-R1 analyzes and extracts strategy logic
3. Generates backtesting.py compatible code
4. Executes backtest and returns performance metrics
5. Cost: ~$0.027 per backtest execution (~6 minutes)

## Common Patterns

### Adding New Agent
1. Create `src/agents/your_agent.py`
2. Implement standalone execution logic
3. Add to `ACTIVE_AGENTS` in `main.py` if needed for orchestration
4. Use `ModelFactory` for LLM calls
5. Store results in `src/data/your_agent/`

### Switching AI Models
Edit `config.py`:
```python
AI_MODEL = "claude-3-haiku-20240307"  # Fast, cheap
# AI_MODEL = "claude-3-sonnet-20240229"  # Balanced
# AI_MODEL = "claude-3-opus-20240229"  # Most powerful
```

Or use different models per agent via ModelFactory:
```python
model = ModelFactory.create_model('deepseek')  # Reasoning tasks
model = ModelFactory.create_model('groq')      # Fast inference
```

### Reading Market Data
```python
from src.nice_funcs import token_overview, get_ohlcv_data, token_price

# Get comprehensive token data
overview = token_overview(token_address)

# Get price history
ohlcv = get_ohlcv_data(token_address, timeframe='1H', days_back=3)

# Get current price
price = token_price(token_address)
```

## Moon Dev YouTube Content Program

### Earning Structure (5+ Minute Videos Only)

| Monthly Views | Earnings per 10,000 Views |
|---------------|---------------------------|
| 10,000 views  | $69 per 10,000 views      |
| 50,000 views  | $100 per 10,000 views     |

**Maximum Earnings**: Up to $1,000 per video, up to $10,000 per month

**Requirements**:
- Videos must be **5 minutes or longer**
- **YouTube ONLY** (no other platforms accepted)

### Source Video Resources

- **Long Videos Dropbox**: https://www.dropbox.com/scl/fo/d0rjdyus9q3pok5nbmo7b/AM9LOmUDv8KIjmH6ypTALx0?rlkey=klg4tinvneqyui46r6851liwa&st=0zxfym3w&dl=0
- **Moon Dev YouTube Channel**: https://www.youtube.com/@moondevonyt/videos (use tools to download)

## Project Philosophy

This is an **experimental, educational project** demonstrating AI agent patterns through algorithmic trading:
- No guarantees of profitability (substantial risk of loss)
- Open source and free for learning
- YouTube-driven development with weekly updates
- Community-supported via Discord
- No token associated with project (avoid scams)

The goal is to democratize AI agent development and show practical multi-agent orchestration patterns that can be applied beyond trading.
