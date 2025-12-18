# MoonView Transition Guide

**Created:** 2025-12-18
**Status:** Planning Phase - Structure Ready

---

## Quick Reference

| Document | Location | Purpose |
|----------|----------|---------|
| **This Doc** | `moon-dev-ai-agents/docs/MOONVIEW_TRANSITION.md` | Transition overview from this project's perspective |
| **Migration Plan** | `moonview/docs/MIGRATION_PLAN.md` | Master migration strategy |
| **Agent Checklist** | `moonview/docs/AGENT_MIGRATION_CHECKLIST.md` | Agent-by-agent tracking |
| **Models Guide** | `moonview/docs/MODELS_MIGRATION_GUIDE.md` | LLM abstraction layer migration |
| **Verification** | `moonview/docs/POST_MIGRATION_VERIFICATION.md` | Testing procedures |
| **Project Docs** | `moonview/docs/PROJECT_DOCUMENTATION.md` | Full moonview documentation |
| **Project Structure** | `moonview/docs/PROJECT_STRUCTURE.md` | File inventory & new structure |

---

## Overview

This project (`moon-dev-ai-agents`) is transitioning to a **reference/upstream sync** role as development consolidates into the **MoonView** project.

### Why the Transition?

**MoonView provides:**
- Professional modular architecture (`src/moonview/`)
- Database integration (PostgreSQL with full schema)
- 32 production-ready strategies
- Real-time streaming (7 data monitors)
- Comprehensive utilities (`utils/` with 20+ modules)
- Single source of truth (ending function duplication)

**moon-dev-ai-agents provides:**
- 56 AI agents (latest Moon Dev code)
- LLM abstraction layer (multi-provider support)
- Upstream sync (auto-merging Moon Dev updates)
- Training materials (ATC Bootcamp Code 2025)

The migration brings the best of both worlds together.

---

## MoonView's New Professional Structure

The moonview project now has a clean, professional structure:

```
moonview/
├── src/                           # Main source code
│   └── moonview/
│       ├── __init__.py
│       ├── core/                  # Core system
│       │   ├── config.py          # All configurations
│       │   ├── constants.py       # Constants, enums
│       │   └── exceptions.py      # Custom exceptions
│       │
│       ├── api/                   # External API integrations
│       │   ├── exchanges/         # Binance, Coinbase, Hyperliquid
│       │   ├── blockchain/        # Etherscan, Solscan, etc.
│       │   └── moondev.py         # MoonDev API
│       │
│       ├── data/                  # Data layer
│       │   ├── database/          # PostgreSQL operations
│       │   ├── streaming/         # WebSocket streams
│       │   └── storage/           # File operations
│       │
│       ├── trading/               # Trading domain
│       │   ├── indicators/        # Technical indicators (ONE source)
│       │   │   ├── trend.py       # SMA, EMA, MACD
│       │   │   ├── momentum.py    # RSI, Stochastic
│       │   │   ├── volatility.py  # ATR, Bollinger
│       │   │   └── volume.py      # OBV, VWAP
│       │   ├── signals.py         # Signal generation
│       │   ├── orders.py          # Order management
│       │   ├── positions.py       # Position tracking
│       │   ├── risk.py            # Risk management
│       │   └── sizing.py          # Position sizing (ONE PLACE!)
│       │
│       ├── wallets/               # Wallet tracking
│       │   ├── tracker.py         # Balance tracking
│       │   ├── whale.py           # Whale detection
│       │   └── discovery.py       # Wallet discovery
│       │
│       └── utils/                 # Pure utilities
│           ├── formatting.py      # Number/date formatting
│           ├── logging.py         # Logging setup
│           ├── security.py        # Key management
│           └── rate_limiter.py    # API rate limiting
│
├── strategies/                    # Trading strategies (32 files)
│   ├── base.py                    # BaseStrategy class
│   ├── breakout/                  # Breakout strategies
│   ├── mean_reversion/            # Mean reversion strategies
│   ├── trend_following/           # Trend strategies
│   └── rbi/                       # RBI system
│
├── monitors/                      # Real-time monitors (from streamline/)
│   ├── open_interest.py
│   ├── funding_rate.py
│   ├── liquidations.py
│   ├── whale_activity.py
│   └── positions.py
│
├── scripts/                       # Standalone scripts
│   ├── daily/                     # Daily scheduled scripts
│   └── migrations/                # One-off migrations
│
├── tests/                         # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── docs/                          # Documentation (comprehensive)
├── config/                        # External configuration
├── credentials/                   # API keys (gitignored)
├── data/                          # Data storage
├── logs/                          # Log files
├── sql/                           # SQL scripts
└── backtest_results/              # Backtest outputs
```

---

## What Gets Migrated

### From `src/models/` → `moonview/src/moonview/models/` (NEW)

| File | Status | Notes |
|------|--------|-------|
| `model_factory.py` | To migrate | Core factory pattern |
| `base_model.py` | To migrate | Abstract base class |
| `claude_model.py` | To migrate | Anthropic Claude |
| `openai_model.py` | To migrate | OpenAI GPT |
| `deepseek_model.py` | To migrate | DeepSeek reasoning |
| `groq_model.py` | To migrate | Groq fast inference |
| `gemini_model.py` | To migrate | Google Gemini |
| `ollama_model.py` | To migrate | Local models |
| `openrouter_model.py` | To migrate | OpenRouter proxy |
| `xai_model.py` | To migrate | xAI Grok |
| `token_tracker.py` | To migrate | Usage tracking |

### From `src/agents/` → `moonview/agents/` (NEW)

**Tier 1 - Essential (4 agents):**
| Agent | Target | Purpose |
|-------|--------|---------|
| `trading_agent.py` | `agents/trading/` | Trade execution |
| `risk_agent.py` | `agents/trading/` | Risk management |
| `strategy_agent.py` | `agents/trading/` | Strategy selection |
| `copybot_agent.py` | `agents/trading/` | Copy trading |

**Tier 2 - Analysis (7 agents):**
| Agent | Target | Purpose |
|-------|--------|---------|
| `sentiment_agent.py` | `agents/analysis/` | Market sentiment |
| `whale_agent.py` | `agents/analysis/` | Whale activity |
| `funding_agent.py` | `agents/analysis/` | Funding rates |
| `liquidation_agent.py` | `agents/analysis/` | Liquidations |
| `chartanalysis_agent.py` | `agents/analysis/` | Technical analysis |
| `volume_agent.py` | `agents/analysis/` | Volume analysis |
| `funding_agent_2.py` | Merge | Into funding_agent.py |

**Tier 3 - Research (3 agents):**
| Agent | Target | Purpose |
|-------|--------|---------|
| `rbi_agent.py` | `agents/research/` | Strategy generation |
| `research_agent.py` | `agents/research/` | Web research |
| `backtest_runner.py` | `agents/research/` | Backtest execution |

**Tier 4 - Content (5 agents):**
| Agent | Target | Purpose |
|-------|--------|---------|
| `chat_agent.py` | `agents/content/` | Interactive chat |
| `clips_agent.py` | `agents/content/` | Video clips |
| `tweet_agent.py` | `agents/content/` | Twitter content |
| `video_agent.py` | `agents/content/` | Video generation |
| `prompt_agent.py` | `agents/content/` | Prompt engineering |

**Tier 5 - Data (7 agents):**
| Agent | Target | Purpose |
|-------|--------|---------|
| `coingecko_agent.py` | `agents/data/` | CoinGecko data |
| `polymarket_agent.py` | `agents/data/` | Prediction markets |
| `polymarket_websearch_agent.py` | `agents/data/` | Enhanced polymarket |
| `scraper_agent.py` | `agents/data/` | Web scraping |
| `websearch_agent.py` | `agents/data/` | Web search |
| `focus_agent.py` | `agents/data/` | Focus tracking |
| `new_or_top_agent.py` | `agents/data/` | Token discovery |

**Tier 6 - Specialized (9 agents):**
| Agent | Target | Purpose |
|-------|--------|---------|
| `sniper_agent.py` | `agents/specialized/` | Token sniping |
| `solana_agent.py` | `agents/specialized/` | Solana-specific |
| `million_agent.py` | `agents/specialized/` | Large trades |
| `tx_agent.py` | `agents/specialized/` | Transaction analysis |
| `compliance_agent.py` | `agents/specialized/` | Compliance |
| `giveaway_agent.py` | `agents/specialized/` | Giveaways |
| `housecoin_agent.py` | `agents/specialized/` | Specific token |
| `listingarb_agent.py` | `agents/specialized/` | Listing arbitrage |
| `fundingarb_agent.py` | `agents/specialized/` | Funding arbitrage |

### NOT Migrating (18 agents)

| Agent | Reason |
|-------|--------|
| `chat_agent_ad.py` | Deprecated |
| `chat_agent_og.py` | Deprecated |
| `rbi_agent_pp.py` | Superseded by rbi_agent.py |
| `rbi_agent_pp_multi.py` | Superseded |
| `rbi_agent_v2.py` | Superseded |
| `rbi_agent_v2_simple.py` | Superseded |
| `rbi_agent_v3.py` | Evaluate if needed |
| `demo_countdown.py` | Demo only |
| `example_unified_agent.py` | Template |
| `phone_agent.py` | Hardware-specific |
| `tiktok_agent.py` | Platform-specific |
| `swarm_agent.py` | Experimental |
| `stream_agent.py` | Unclear purpose |
| `realtime_clips_agent.py` | Merge into clips_agent |
| `shortvid_agent.py` | Merge into video_agent |
| `rbi_batch_backtester.py` | Merge into backtest_runner |
| `clean_ideas.py` | Utility script |
| `code_runner_agent.py` | Security risk |

---

## Utility Function Mapping

### From `nice_funcs.py` → MoonView Modules

| Function | moon-dev-ai-agents | MoonView Target |
|----------|-------------------|-----------------|
| `token_overview()` | `nice_funcs.py` | `moonview.api.exchanges` |
| `token_price()` | `nice_funcs.py` | `moonview.api.exchanges` |
| `get_position()` | `nice_funcs.py` | `moonview.trading.positions` |
| `get_ohlcv_data()` | `nice_funcs.py` | `moonview.data.database` |
| `market_buy/sell()` | `nice_funcs.py` | `moonview.trading.orders` |
| `chunk_kill()` | `nice_funcs.py` | `moonview.trading.orders` |
| `calculate_position_size()` | 18 files! | `moonview.trading.sizing` (ONE PLACE) |
| `calculate_rsi()` | 9 files | `moonview.trading.indicators.momentum` |
| `calculate_sma()` | 8 files | `moonview.trading.indicators.trend` |

### From `src/config.py` → MoonView Config

| Setting | Target |
|---------|--------|
| `MONITORED_TOKENS` | `config/__init__.py` (CRYPTO_METADATA) |
| `EXCLUDED_TOKENS` | `config/__init__.py` |
| Position sizing | `moonview.trading.sizing` |
| Risk limits | `moonview.trading.risk` |
| AI settings | New `config/ai.py` module |

---

## Shared Resources (Already Unified)

| Resource | Mechanism | Status |
|----------|-----------|--------|
| Python environment | `.moonview_env` symlink | Working |
| API credentials | `credentials/api_secrets.py` | Working |
| Config module | `config/__init__.py` | Working |
| Data folder | `data/` structure | Working |

---

## Migration Phases

### Phase 1: Foundation (In Progress)

MoonView agent is creating:
- [x] `src/moonview/` directory structure
- [x] `src/moonview/core/` - config, constants, exceptions
- [x] `src/moonview/api/` - exchange and blockchain integrations
- [x] `src/moonview/data/` - database and storage
- [x] `src/moonview/trading/` - indicators, orders, positions, risk
- [x] `src/moonview/wallets/` - wallet tracking
- [x] `src/moonview/utils/` - pure utilities
- [x] `monitors/` - real-time monitors
- [x] `scripts/` - standalone scripts
- [x] `tests/` - test suite structure
- [x] `docs/PROJECT_DOCUMENTATION.md` - comprehensive docs
- [x] `docs/PROJECT_STRUCTURE.md` - file inventory

### Phase 2: Models Migration (Next)

After moonview structure is complete:
1. Create `moonview/models/` directory
2. Copy model files from `moon-dev-ai-agents/src/models/`
3. Update imports to use moonview credentials
4. Test all providers work

### Phase 3: Agents Migration

After models are working:
1. Create `moonview/agents/` directory structure
2. Migrate Tier 1 agents (trading, risk, strategy)
3. Migrate Tier 2 agents (analysis)
4. Migrate remaining tiers
5. Update imports to use moonview modules

### Phase 4: Integration & Testing

1. Wire agents to moonview database
2. Integrate with monitors
3. Create unified orchestrator
4. Run verification tests

### Phase 5: Finalization

1. Update all documentation
2. Mark moon-dev-ai-agents as reference-only
3. Update this project's CLAUDE.md

---

## Post-Migration: This Project's Role

After migration completes, moon-dev-ai-agents will serve as:

1. **Upstream Sync Target**
   - Continue auto-merging Moon Dev updates via `sync_upstream_daily.sh`
   - New agents/features appear here first

2. **Reference Codebase**
   - Check for new agent implementations
   - Compare against original Moon Dev code

3. **Training Materials**
   - ATC Bootcamp Code 2025 remains here
   - Educational content for learning

4. **Experimental Sandbox**
   - Test new ideas before adding to MoonView
   - Keep experimental agents here

---

## Import Path Changes

When migrating agents, update imports:

```python
# OLD (moon-dev-ai-agents)
from src.models.model_factory import ModelFactory
from src.agents.api import MoonDevAPI
from src.config import *
from src.nice_funcs import token_overview, get_ohlcv_data

# NEW (moonview)
from models import ModelFactory
from agents.api import MoonDevAPI
from config import CRYPTO_METADATA, API_ENDPOINTS
from moonview.trading.indicators.momentum import calculate_rsi
from moonview.trading.sizing import calculate_position_size
from moonview.data.database import get_ohlcv_data
```

---

## Quick Commands

```bash
# View moonview documentation
cat ~/WorkLocal/moonview/docs/PROJECT_DOCUMENTATION.md

# View moonview structure
cat ~/WorkLocal/moonview/docs/PROJECT_STRUCTURE.md

# View migration plan
cat ~/WorkLocal/moonview/docs/MIGRATION_PLAN.md

# Check moonview new structure
ls -la ~/WorkLocal/moonview/src/moonview/

# Check if agents/ exists yet
ls -la ~/WorkLocal/moonview/agents/ 2>/dev/null || echo "Not yet created"

# Check if models/ exists yet
ls -la ~/WorkLocal/moonview/models/ 2>/dev/null || echo "Not yet created"
```

---

## Checklist: Before Starting Migration

- [ ] Moonview agent has completed structure setup
- [ ] All `src/moonview/` subdirectories created
- [ ] `monitors/` directory populated
- [ ] `tests/` structure complete
- [ ] `docs/PROJECT_DOCUMENTATION.md` finalized
- [ ] `docs/PROJECT_STRUCTURE.md` finalized
- [ ] Review moonview CLAUDE.md for instructions

---

## Questions?

The complete migration documentation lives in `~/WorkLocal/moonview/docs/`:
- `MIGRATION_PLAN.md` - Master strategy
- `AGENT_MIGRATION_CHECKLIST.md` - Agent-by-agent tracking
- `MODELS_MIGRATION_GUIDE.md` - LLM layer migration
- `POST_MIGRATION_VERIFICATION.md` - Testing procedures
- `PROJECT_DOCUMENTATION.md` - Full project documentation
- `PROJECT_STRUCTURE.md` - File inventory and new structure
