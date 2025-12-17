# ATC Bootcamp 2025 - Course Recovery Guide

**Created:** 2025-12-12
**Purpose:** Get you back on track after completing Days 1-15

---

## Quick Status Summary

| Item | Status |
|------|--------|
| **Days Completed** | 1-15 (including Day 13 Backtesting + OpenAI Assistants) |
| **Current Position** | Ready for Day 16+ content |
| **Bootcamp Location** | `ATC Bootcamp Code 2025/` |
| **Personal Project** | `~/WorkLocal/MoonView/` |
| **Main Project** | `~/WorkLocal/moon-dev-ai-agents/` |

---

## What You've Already Learned (Days 1-15)

### Foundation (Days 1-4)
- [x] **Day 2**: Coding basics (`2_coding_basics.py`, `2.1-anaconda-pip-vsc.py`)
- [x] **Day 2 Projects**: Data streams (liquidations, funding, trades) + productivity app
- [x] **Day 4**: Algorithmic orders (`4-algo_orders.py`)

### Risk & Indicators (Days 5-9)
- [x] **Day 5**: Risk management (`5_risk/5_risk.py`, `5_risk_mgmt_hl.py`)
- [x] **Day 6**: SMA indicator (`6_sma.py`)
- [x] **Day 7**: RSI indicator (`7_rsi.py`)
- [x] **Day 8**: VWAP indicator (`8_vwap.py`)
- [x] **Day 9**: More indicators - VWMA, pandas_ta, talib (`9_more_indicators/`)

### Trading Bots (Days 10-12)
- [x] **Day 10**: First bot - Bollinger Band bot (`10_day10_bots/`)
- [x] **Day 11**: Second bot - SDZ bot (`11_day11_bots/`)
- [x] **Day 12**: Third bot - VWAP bot (`12_day12_bots/`)

### Backtesting & AI (Days 13-15)
- [x] **Day 13**: Backtesting with Backtrader (`13_backtesting.py`)
- [x] **Days 14-15**: OpenAI Assistants for algo trading (`Open-AI-Assistants for Bootcamp Members Only/`)
  - RBI System (Research-Backtest-Implement)
  - AI traders 1-6 (progressive complexity)
  - Auto-generating strategies from ideas
  - Looping through indicator combinations

---

## Your Personal Work Summary

### MoonView Project (`~/WorkLocal/MoonView/`)

**What you built:**
- Custom trading strategy framework
- 40+ strategy files including:
  - `15_algorithms_that_work.py`
  - `25_algorithm_integration.py`
  - `Algorithm_Catalog.py`
  - Multiple strategies: SMA_Cross, RSI_Trend, Turtle_Trading, VWAP_EMA_ADX, etc.
- Database integration (Supabase, PostgreSQL)
- Data pipeline for multiple exchanges (Binance, Coinbase, HyperLiquid)
- Backtest results storage
- Daily/Strategy automation scripts

**Key Config Settings:**
```python
# From config.py
SUPABASE_ENABLED = False
DB_ENABLED = True
WHALE_THRESHOLD = 1000  # BTC
LARGE_TX_THRESHOLD = 250000  # $250K USD
```

**To restart MoonView:**
```bash
cd ~/WorkLocal/MoonView
source .moonview_env/bin/activate  # or conda activate tflow
python start_daily.sh  # or start_strategy.sh
```

---

## Resources Available

### Dropbox Course Materials
**URL:** https://www.dropbox.com/scl/fo/d0rjdyus9q3pok5nbmo7b/AM9LOmUDv8KIjmH6ypTALx0?rlkey=klg4tinvneqyui46r6851liwa&st=0zxfym3w&dl=0

Contains:
- Long-form videos for content creation
- Course materials beyond what's in the bootcamp folder
- Additional resources

### YouTube Channel
**URL:** https://www.youtube.com/@moondevonyt

### Content Creation Opportunity
- **5+ minute videos**: $69-$100 per 10,000 views
- **Max earnings**: $1,000/video, $10,000/month
- Use Dropbox videos as source material

---

## Day 16+ Content Overview

Based on the bootcamp structure and main project, here's what comes next:

### Immediate Next Steps (Day 16+)

#### 1. Advanced AI Trading (RBI Agent Deep Dive)
**Location:** `src/agents/rbi_agent.py` in main project

The RBI system you learned in Days 14-15 has been expanded into a full agent:
- Research from YouTube videos, PDFs, text
- Uses DeepSeek-R1 for strategy extraction
- Auto-generates backtesting.py code
- Executes and reports performance

```bash
# Try it out
cd ~/WorkLocal/moon-dev-ai-agents
conda activate tflow
python src/agents/rbi_agent.py
```

#### 2. Model Factory Pattern
**Location:** `src/models/model_factory.py`

Learn to use multiple AI providers:
```python
from src.models.model_factory import ModelFactory

# Switch between providers easily
model = ModelFactory.create_model('anthropic')  # Claude
model = ModelFactory.create_model('openai')     # GPT-4
model = ModelFactory.create_model('deepseek')   # DeepSeek
model = ModelFactory.create_model('groq')       # Groq (fast)
```

#### 3. Swarm Agent (Multi-Model Consensus)
**Location:** `src/agents/swarm_agent.py`

Run 7+ AI models simultaneously and get consensus:
- Claude, Opus, OpenAI, Groq, Gemini, DeepSeek, XAI
- Weighted voting for trading decisions

#### 4. Data Sources 2025
**Location:** `2025 Data Sources/`

Updated data fetching scripts:
- `coinbase_data_2025.py` - 70+ weeks of data
- `data_from_hl_2025.py` - HyperLiquid (5000 bar limit)

### Bonus Content Available

**Location:** `ATC Bootcamp Code 2025/Bonus_algos_6ofthem/`

1. **Turtle Trending Algo** - Classic trend following
2. **Correlation Algo** - Pair trading
3. **Consolidation Pop Algo** - Breakout strategy
4. **Nadarya Watson Algo** - Kernel regression
5. **Market Maker** - Spread capture
6. **Mean Reversion** - 74 tickers strategy

**HyperLiquid Trading Bots:**
**Location:** `ATC Bootcamp Code 2025/HyperLiquid-Trading-Bots - Members only/`
- Arbitrage bot (`arb.py`)
- HyperLiquid-specific utilities

---

## Recovery Action Plan

### This Week: Review & Refresh

#### Day 1: Quick Review (2-3 hours)
```bash
# 1. Review your bootcamp progress
cd ~/WorkLocal/moon-dev-ai-agents
ls "ATC Bootcamp Code 2025/"

# 2. Run a simple backtest to refresh memory
python "ATC Bootcamp Code 2025/13_backtesting.py"

# 3. Review the RBI system README
cat "ATC Bootcamp Code 2025/Open-AI-Assistants for Bootcamp Members Only/README.md"
```

#### Day 2: Run Modern Agents (2-3 hours)
```bash
conda activate tflow

# Test the updated RBI agent
python src/agents/rbi_agent.py

# Try the swarm agent
python src/agents/swarm_agent.py

# Check polymarket agent
python src/agents/polymarket_websearch_agent.py
```

#### Day 3: Explore Your MoonView Project (2-3 hours)
```bash
cd ~/WorkLocal/MoonView

# Review what you built
ls strategies/
cat config.py | head -100

# Check your backtest results
ls backtest_results/
```

#### Day 4-5: Continue with New Content
- Work through bonus algos
- Integrate learnings into MoonView
- Start building custom agents

---

## Key Files Quick Reference

### Bootcamp Code (Review These First)
```
ATC Bootcamp Code 2025/
├── 13_backtesting.py              # Backtrader basics
├── Open-AI-Assistants/
│   ├── README.md                  # RBI system explained
│   ├── ai_trader6.py              # Most advanced AI trader
│   └── bt_code/                   # Generated backtests
├── Bonus_algos_6ofthem/           # 6 complete strategies
└── datasets/                      # BTC data for testing
```

### Main Project (New Since Day 15)
```
src/
├── agents/
│   ├── rbi_agent.py               # Enhanced RBI system
│   ├── swarm_agent.py             # Multi-model consensus
│   ├── polymarket_websearch_agent.py  # Prediction markets
│   └── funding_agent_2.py         # HyperLiquid funding
├── models/
│   └── model_factory.py           # Multi-provider AI
└── 2025 Data Sources/             # Updated data fetchers
```

### Your Personal Project
```
~/WorkLocal/MoonView/
├── strategies/                    # 40+ strategies you built
├── config.py                      # Your configuration
├── start_daily.sh                 # Automation scripts
└── streamline/                    # Data pipelines
```

---

## Environment Setup Reminder

```bash
# Always use this environment
conda activate tflow

# Project location
cd ~/WorkLocal/moon-dev-ai-agents

# Check your API keys are set
cat .env | grep -E "^[A-Z].*=" | head -10
# Should show: ANTHROPIC_KEY, OPENAI_KEY, etc. (values hidden)
```

---

## Questions to Answer as You Continue

1. **What strategies from MoonView performed best?**
   - Review `~/WorkLocal/MoonView/backtest_results/`

2. **Which AI model works best for strategy generation?**
   - Test different models via ModelFactory

3. **Can you combine your MoonView strategies with the RBI agent?**
   - Import your strategies into the main project

4. **What new indicators or patterns do you want to test?**
   - Use the bonus algos as templates

---

## Next Session Checklist

- [ ] Read this document completely
- [ ] Run `13_backtesting.py` to refresh backtest knowledge
- [ ] Run `rbi_agent.py` to see the enhanced system
- [ ] Review your MoonView strategies
- [ ] Pick 1 bonus algo to study in depth
- [ ] Update CLAUDE.md if you discover new patterns

---

**Remember:** The goal is to build AI agents that trade for you. You have all the foundation - now it's about refinement and integration.

**Moon Dev's Philosophy:** R-B-I (Research-Backtest-Implement) running 24/7 with AI.
