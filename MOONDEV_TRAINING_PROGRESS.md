# Moon Dev AI Agents Training Progress

**Last Updated:** 2025-12-12

---

## Resources Access

### Moon Dev YouTube Channel
- **URL:** https://www.youtube.com/@moondevonyt
- **Status:** Subscribed and following updates

### Moon Dev Dropbox (Course Materials)
- **URL:** https://www.dropbox.com/scl/fo/d0rjdyus9q3pok5nbmo7b/AM9LOmUDv8KIjmH6ypTALx0?rlkey=klg4tinvneqyui46r6851liwa&e=3&st=0zxfym3w&dl=0
- **Access:** Granted
- **Contents:** Training materials, code examples, additional resources for the ATC Bootcamp

---

## Training Progress: Days 1-15 (Completed)

### Summary of Code Added

Based on git history analysis, the following major additions have been made:

---

### 2025 Data Sources (NEW FOLDER)

| File | Purpose | Key Features |
|------|---------|--------------|
| `2025 Data Sources/coinbase_data_2025.py` | Fetch historical OHLCV data from Coinbase Exchange API | Supports multiple symbols (BTC-USD, ETH-USD, SOL-USD), configurable timeframes (1m to 1d), fetches up to 70+ weeks of data, handles rate limits |
| `2025 Data Sources/data_from_hl_2025.py` | Fetch historical OHLCV data from HyperLiquid API | Max 5000 bars per request (API limit), handles timestamp offset bug, supports all HL symbols |

**Usage Notes:**
- Coinbase script requires `COINBASE_API_KEY` and `COINBASE_API_SECRET` in `.env`
- HyperLiquid has a hard limit of 5000 candles - use Coinbase for longer history
- Data saves to `data/coinbase/` or `data/` directories

---

### New Agents Added

#### 1. Polymarket WebSearch Agent
- **File:** `src/agents/polymarket_websearch_agent.py`
- **Lines:** ~1,440
- **Purpose:** Tracks Polymarket prediction market whale trades with real-time web search enrichment
- **Key Features:**
  - WebSocket connection to Polymarket live trading feed
  - OpenAI `gpt-4o-mini-search-preview` for web search context
  - AI swarm consensus (7 models: Claude, Opus, OpenAI, Groq, Gemini, DeepSeek, XAI)
  - Filters $500+ trades, excludes crypto/sports markets
- **Data Output:** `src/data/polymarket_websearch/`
- **Docs:** See `docs/polymarket_agents.md`

#### 2. Scraper Agent
- **File:** `src/agents/scraper_agent.py`
- **Lines:** ~686
- **Purpose:** Batch website scraper with AI analysis
- **Key Features:**
  - Selenium headless browser (handles JS-rendered sites)
  - Parallel batch processing
  - SwarmAgent or XAI model analysis
  - Multiple output formats (JSON, TXT, raw)
- **Data Output:** `src/data/scraper_agent/`
- **Docs:** `docs/scraper_agent.md`

#### 3. Giveaway Agent
- **File:** `src/agents/giveaway_agent.py`
- **Lines:** ~340
- **Purpose:** Track stream chat participation for giveaways
- **Key Features:**
  - Multi-platform via Restream (YouTube, Twitch, X)
  - Point-based system (1 point per message 10+ chars)
  - 777 bonus trigger with cooldown
  - Solana wallet collection
- **Data Output:** `src/data/giveaway_agent/participants.csv`
- **Docs:** `docs/giveaway_agent.md`
- **Requires:** `RESTREAM_EMBED_TOKEN` in `.env`

#### 4. Funding Agent 2
- **File:** `src/agents/funding_agent_2.py`
- **Lines:** ~311
- **Purpose:** Scans HyperLiquid for funding rate anomalies with voice announcements
- **Key Features:**
  - Fetches ALL HyperLiquid symbols
  - Calculates hourly and annualized funding rates
  - Top 3 positive/negative rate identification
  - OpenAI TTS voice announcements
- **Data Output:** `src/data/funding_agent_2/` + `src/audio/`
- **Scan Interval:** 15 minutes

---

### New Scripts Added

#### HyperLiquid Data Fetcher
- **File:** `src/scripts/hyperliquid_data.py`
- **Lines:** ~196
- **Purpose:** Standalone script to download historical OHLCV from HyperLiquid
- **Key Features:**
  - Up to 5,000 candles per request (API max)
  - Timestamp offset correction
  - Configurable symbol/timeframe
  - Auto-retry logic
- **Data Output:** `src/data/hyperliquid_data/`

#### ADX VWAP Backtest
- **File:** `src/scripts/backtest_adx_vwap.py`
- **Purpose:** Backtest strategy combining ADX and VWAP indicators

---

### Updated Components

#### Model Factory Updates
- **File:** `src/models/model_factory.py`
- Added support for new models including Opus 4.5

#### Swarm Agent Updates
- **File:** `src/agents/swarm_agent.py`
- Implemented Opus 4.5 model integration
- Enhanced multi-model consensus

#### Liquidation Agent Updates
- **File:** `src/agents/liquidation_agent.py`
- Updated data sources and processing

#### RBI Agent Updates
- **Files:** `src/agents/rbi_agent.py`, `rbi_agent_pp.py`, `rbi_agent_v2.py`, `rbi_agent_v3.py`, `rbi_agent_pp_multi.py`
- Path fixes for better compatibility
- PDF/YouTube extraction improvements

---

### Removed/Cleaned Up

The `src/quant/` directory was removed in recent commits. Files that were cleaned up:
- `src/quant/2xmareversal.py`
- `src/quant/BTCUSD-1d-100wks-data.csv`
- `src/quant/README.md`
- `src/quant/nice_funcs*.py`
- `src/quant/pure_liquidation_momentum.py`
- `src/quant/liq_data_BTC_5m_ohlcv.csv`

---

## Documentation Status

### Existing Docs (in `docs/` folder)
| Document | Status |
|----------|--------|
| giveaway_agent.md | Complete |
| scraper_agent.md | Complete |
| polymarket_agents.md | Exists (covers both polymarket agents) |
| funding_agent.md | Exists (may need update for agent 2) |
| All other agent docs | Exist |

### Personal Docs (root folder)
| Document | Status |
|----------|--------|
| START_HERE.md | Complete |
| CLAUDE.md | Updated |
| ANALYSIS.md | Complete |
| GIT_WORKFLOW.md | Complete |
| GIT_QUICK_REFERENCE.md | Complete |
| README_PADI.md | Complete |

---

## Git Workflow Status

- **Main Branch:** `main`
- **Upstream:** Moon Dev's original repo
- **Origin:** Your fork
- **Auto-sync:** Daily automation configured (`sync_upstream_daily.sh`)
- **Last Upstream Merge:** 2025-11-28

---

## Environment Setup Checklist

### Required API Keys (in `.env`)
```
# AI Models
ANTHROPIC_KEY=         # Claude API
OPENAI_KEY=            # OpenAI + TTS
DEEPSEEK_KEY=          # DeepSeek
GROQ_API_KEY=          # Groq
GEMINI_KEY=            # Google Gemini

# Trading/Data
BIRDEYE_API_KEY=       # Solana token data
MOONDEV_API_KEY=       # Moon Dev API
COINGECKO_API_KEY=     # Token metadata

# Blockchain
SOLANA_PRIVATE_KEY=    # Solana wallet
HYPER_LIQUID_ETH_PRIVATE_KEY=  # HyperLiquid
RPC_ENDPOINT=          # Helius RPC

# New for 2025
COINBASE_API_KEY=      # Coinbase data fetching
COINBASE_API_SECRET=   # Coinbase API secret
RESTREAM_EMBED_TOKEN=  # Giveaway agent
```

### Conda Environment
```bash
conda activate tflow
```

---

## Next Steps

1. [ ] Review ATC Bootcamp materials from Dropbox
2. [ ] Continue with training days 16+
3. [ ] Test new data sources (Coinbase, HyperLiquid 2025)
4. [ ] Explore polymarket websearch agent capabilities
5. [ ] Set up any missing API keys

---

## Quick Reference: Running Agents

```bash
# Data fetching
python "2025 Data Sources/coinbase_data_2025.py"
python "2025 Data Sources/data_from_hl_2025.py"

# New agents
python src/agents/polymarket_websearch_agent.py
python src/agents/scraper_agent.py
python src/agents/giveaway_agent.py
python src/agents/funding_agent_2.py

# Scripts
python src/scripts/hyperliquid_data.py
```

---

**Document maintained by:** Claude Code Assistant
**Project:** Moon Dev AI Agents Fork
**Location:** `/Users/padilla/WorkLocal/moon-dev-ai-agents`
