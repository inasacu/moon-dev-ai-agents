# Moon Dev AI Agents - Project Structure & File Inventory

**Last Updated:** 2025-12-18
**Purpose:** Comprehensive file inventory for migration to MoonView

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [File Statistics](#file-statistics)
3. [Source Code Inventory](#source-code-inventory)
4. [Function Duplication Report](#function-duplication-report)
5. [MoonView Overlap Analysis](#moonview-overlap-analysis)
6. [Migration Decision Matrix](#migration-decision-matrix)
7. [Proposed Target Structure](#proposed-target-structure)

---

## Executive Summary

### Key Findings

1. **4 utility files with duplicated trading functions** - nice_funcs*.py files share similar patterns
2. **58 agent files** - 38 to migrate, 20 deprecated/skip
3. **10 LLM model files** - All need migration (moonview doesn't have these)
4. **Significant function overlap** with moonview utilities

### Migration Complexity

| Category | Files | Complexity | Notes |
|----------|-------|------------|-------|
| Models | 12 | Low | Direct copy with import updates |
| Core Agents | 17 | Medium | Update imports, integrate with moonview |
| Analysis Agents | 7 | Medium | Connect to moonview monitors |
| Research Agents | 3 | Medium | Integrate with moonview strategies |
| Content Agents | 5 | Low | Standalone, minimal dependencies |
| Data Agents | 7 | Low | Standalone, use models |
| Specialized Agents | 9 | Medium | Various dependencies |
| Utilities | 4 | High | Decompose to moonview modules |

---

## File Statistics

### Source Code Summary

| Category | Files | Total Lines | Avg Lines/File |
|----------|-------|-------------|----------------|
| Agents | 58 | 32,500 | 560 |
| Models | 12 | 1,500 | 125 |
| Utilities (nice_funcs*) | 4 | 3,795 | 949 |
| Core (config, main, etc.) | 4 | 942 | 236 |
| Scripts | 25 | 3,275 | 131 |
| **Total** | **103** | **~42,000** | - |

### Files by Size (Top 20)

| File | Lines | Category |
|------|-------|----------|
| `agents/rbi_agent_pp_multi.py` | 1,838 | Deprecated |
| `agents/polymarket_agent.py` | 1,485 | Data |
| `agents/polymarket_websearch_agent.py` | 1,440 | Data |
| `agents/rbi_agent_pp.py` | 1,313 | Deprecated |
| `agents/tiktok_agent.py` | 1,288 | Skip |
| `agents/websearch_agent.py` | 1,280 | Data |
| `agents/trading_agent.py` | 1,195 | Trading |
| `nice_funcs.py` | 1,183 | Utility |
| `agents/rbi_agent_v3.py` | 1,167 | Evaluate |
| `agents/chat_agent_og.py` | 1,111 | Deprecated |
| `agents/rbi_agent.py` | 1,049 | Research |
| `agents/chat_agent_ad.py` | 1,018 | Deprecated |
| `agents/code_runner_agent.py` | 941 | Skip |
| `nice_funcs_hyperliquid.py` | 924 | Utility |
| `agents/realtime_clips_agent.py` | 875 | Merge |
| `agents/rbi_agent_v2.py` | 874 | Deprecated |
| `nice_funcs_extended.py` | 851 | Utility |
| `nice_funcs_aster.py` | 837 | Utility |
| `agents/phone_agent.py` | 797 | Skip |
| `agents/listingarb_agent.py` | 762 | Specialized |

---

## Source Code Inventory

### `src/` Root Files

| File | Lines | Description | Functions/Classes | Migration |
|------|-------|-------------|-------------------|-----------|
| `__init__.py` | 0 | Package init | - | Skip |
| `config.py` | ~100 | Trading config | 30+ constants | Merge to moonview config |
| `main.py` | ~200 | Orchestrator | `main()`, agent loop | `agents/orchestrator.py` |
| `exchange_manager.py` | 381 | Multi-exchange | `ExchangeManager` class | `moonview.api.exchanges` |
| `ezbot.py` | 261 | Legacy controller | `EZBot` class | Evaluate |

---

### `src/nice_funcs.py` (1,183 lines) - Solana Trading

**Purpose:** Core trading utilities for Solana/Jupiter

| Function | Lines | Purpose | MoonView Target |
|----------|-------|---------|-----------------|
| `cleanup_temp_data()` | 10 | Clean temp files | `moonview.utils` |
| `print_pretty_json(data)` | 5 | JSON formatting | `moonview.utils.formatting` |
| `find_urls(string)` | 10 | URL extraction | `moonview.utils` |
| `token_overview(address)` | 30 | Token metadata | `moonview.api.blockchain.solana` |
| `token_security_info(address)` | 25 | Security check | `moonview.api.blockchain.solana` |
| `token_creation_info(address)` | 20 | Creation info | `moonview.api.blockchain.solana` |
| `market_buy(token, amount, slippage)` | 40 | Execute buy | `moonview.trading.orders` |
| `market_sell(token, amount, slippage)` | 40 | Execute sell | `moonview.trading.orders` |
| `get_time_range(days_back)` | 15 | Time range calc | `moonview.utils.formatting` |
| `round_down(value, decimals)` | 5 | Round down | `moonview.utils.formatting` |
| `get_data(address, days, timeframe)` | 50 | Get OHLCV | `moonview.data.database` |
| `fetch_wallet_holdings_og(address)` | 30 | Wallet holdings | `moonview.wallets.tracker` |
| `fetch_wallet_token_single(address, token)` | 25 | Single token | `moonview.wallets.tracker` |
| `token_price(address)` | 20 | Current price | `moonview.api.blockchain.solana` |
| `get_position(token)` | 35 | Position info | `moonview.trading.positions` |
| `get_decimals(token)` | 15 | Token decimals | `moonview.api.blockchain.solana` |
| `pnl_close(token)` | 40 | P&L based close | `moonview.trading.risk` |
| `chunk_kill(token, max_size, slippage)` | 50 | Gradual close | `moonview.trading.orders` |
| `sell_token(token, amount, slippage)` | 30 | Sell specific | `moonview.trading.orders` |
| `kill_switch(token)` | 20 | Emergency close | `moonview.trading.risk` |
| `close_all_positions()` | 30 | Close all | `moonview.trading.positions` |
| `supply_demand_zones(token, tf, limit)` | 60 | S/D zones | `moonview.trading.signals` |
| `elegant_entry(symbol, buy_under)` | 40 | Entry logic | `moonview.trading.signals` |
| `breakout_entry(symbol, price)` | 35 | Breakout entry | `moonview.trading.signals` |
| `ai_entry(symbol, amount)` | 45 | AI-based entry | `moonview.trading.signals` |
| `get_token_balance_usd(token)` | 25 | USD balance | `moonview.trading.positions` |

---

### `src/nice_funcs_hyperliquid.py` (924 lines) - HyperLiquid

**Purpose:** Trading utilities for HyperLiquid perpetuals

| Function | Lines | Purpose | MoonView Target |
|----------|-------|---------|-----------------|
| `adjust_timestamp(dt)` | 10 | Timestamp fix | `moonview.utils.formatting` |
| `ask_bid(symbol)` | 25 | Order book | `moonview.trading.market_data` |
| `get_sz_px_decimals(symbol)` | 20 | Size/price decimals | `moonview.api.exchanges.hyperliquid` |
| `get_position(symbol, account)` | 35 | Position info | `moonview.trading.positions` |
| `set_leverage(symbol, leverage, account)` | 25 | Set leverage | `moonview.trading.leverage` |
| `adjust_leverage_usd_size(...)` | 30 | Leverage calc | `moonview.trading.leverage` |
| `cancel_all_orders(account)` | 20 | Cancel orders | `moonview.trading.orders` |
| `limit_order(coin, is_buy, sz, px, ...)` | 50 | Limit order | `moonview.trading.orders` |
| `kill_switch(symbol, account)` | 30 | Emergency close | `moonview.trading.risk` |
| `pnl_close(symbol, target, max_loss, ...)` | 60 | P&L close | `moonview.trading.risk` |
| `get_current_price(symbol)` | 15 | Current price | `moonview.trading.market_data` |
| `get_account_value(account)` | 20 | Account value | `moonview.trading.positions` |
| `market_buy(symbol, usd_size, account)` | 35 | Market buy | `moonview.trading.orders` |
| `market_sell(symbol, usd_size, account)` | 35 | Market sell | `moonview.trading.orders` |
| `close_position(symbol, account)` | 25 | Close position | `moonview.trading.positions` |
| `get_balance(account)` | 15 | Get balance | `moonview.trading.positions` |
| `get_all_positions(account)` | 30 | All positions | `moonview.trading.positions` |
| `_get_exchange()` | 10 | Exchange instance | `moonview.api.exchanges.hyperliquid` |
| `_get_info()` | 10 | Exchange info | `moonview.api.exchanges.hyperliquid` |
| `_get_ohlcv(...)` | 40 | Raw OHLCV | `moonview.data.database` |
| `_process_data_to_df(data)` | 30 | Process to DF | `moonview.data.database` |
| `add_technical_indicators(df)` | 80 | Add TA | `moonview.trading.indicators` |
| `get_data(symbol, timeframe, bars, ...)` | 50 | Get OHLCV+TA | `moonview.data.database` |
| `get_market_info()` | 20 | Market info | `moonview.api.exchanges.hyperliquid` |
| `get_funding_rates(symbol)` | 25 | Funding rates | `moonview.api.exchanges.hyperliquid` |
| `ai_entry(symbol, amount, ...)` | 60 | AI entry | `moonview.trading.signals` |
| `open_short(token, amount, ...)` | 45 | Open short | `moonview.trading.orders` |

---

### `src/nice_funcs_extended.py` (851 lines) - X10 Exchange

**Purpose:** Trading utilities for X10 exchange

| Class/Function | Lines | Purpose | MoonView Target |
|----------------|-------|---------|-----------------|
| `ExtendedExchangeAPI` | 400 | API wrapper | `moonview.api.exchanges.x10` |
| `__init__(api_key, private_key, ...)` | 30 | Initialize | - |
| `_request(method, endpoint, data)` | 50 | HTTP request | - |
| `get_account_info()` | 20 | Account info | - |
| `get_position(symbol)` | 25 | Position info | - |
| `set_leverage(symbol, leverage)` | 20 | Set leverage | - |
| `buy_limit(symbol, qty, price, ...)` | 30 | Limit buy | - |
| `sell_limit(symbol, qty, price, ...)` | 30 | Limit sell | - |
| `buy_market(symbol, qty, ...)` | 25 | Market buy | - |
| `sell_market(symbol, qty, ...)` | 25 | Market sell | - |
| `cancel_all_orders(symbol)` | 20 | Cancel orders | - |
| `close_position(symbol)` | 25 | Close position | - |
| `get_account_balance()` | 20 | Get balance | `moonview.trading.positions` |
| `get_position(symbol)` | 25 | Position info | `moonview.trading.positions` |
| `market_buy(symbol, usd_amount, ...)` | 35 | Market buy | `moonview.trading.orders` |
| `market_sell(symbol, usd_amount, ...)` | 35 | Market sell | `moonview.trading.orders` |
| `open_long(symbol, usd_amount, ...)` | 30 | Open long | `moonview.trading.orders` |
| `open_short(symbol, usd_amount, ...)` | 30 | Open short | `moonview.trading.orders` |
| `close_position(symbol)` | 25 | Close position | `moonview.trading.positions` |
| `chunk_kill(symbol, max_chunk, ...)` | 50 | Gradual close | `moonview.trading.orders` |

---

### `src/nice_funcs_aster.py` (837 lines) - Aster Exchange

**Purpose:** Trading utilities for Aster exchange

Similar pattern to `nice_funcs_extended.py`.

---

### `src/models/` - LLM Abstraction Layer

| File | Lines | Classes | Migration |
|------|-------|---------|-----------|
| `__init__.py` | 30 | - | Update imports |
| `base_model.py` | 100 | `ModelResponse`, `BaseModel` | Direct copy |
| `model_factory.py` | 150 | `ModelFactory` | Direct copy |
| `claude_model.py` | 120 | `ClaudeModel` | Direct copy |
| `openai_model.py` | 440 | `OpenAIModel` | Direct copy |
| `deepseek_model.py` | 100 | `DeepSeekModel` | Direct copy |
| `groq_model.py` | 100 | `GroqModel` | Direct copy |
| `gemini_model.py` | 100 | `GeminiModel` | Direct copy |
| `ollama_model.py` | 100 | `OllamaModel` | Direct copy |
| `openrouter_model.py` | 100 | `OpenRouterModel` | Direct copy |
| `xai_model.py` | 80 | `XAIModel` | Direct copy |
| `token_tracker.py` | 200 | `TokenTracker` | Direct copy |

---

### `src/agents/` - Agent Files

#### Trading Agents

| File | Lines | Key Classes/Functions | MoonView Target |
|------|-------|----------------------|-----------------|
| `trading_agent.py` | 1,195 | `TradingAgent`, `analyze_market`, `execute_trade` | `agents/trading/` |
| `risk_agent.py` | 631 | `RiskAgent`, `check_risk`, `close_if_breach` | `agents/trading/` |
| `strategy_agent.py` | 305 | `StrategyAgent`, `select_strategy`, `generate_signals` | `agents/trading/` |
| `copybot_agent.py` | 326 | `CopybotAgent`, `copy_trade`, `monitor_wallets` | `agents/trading/` |

#### Analysis Agents

| File | Lines | Key Classes/Functions | MoonView Target |
|------|-------|----------------------|-----------------|
| `sentiment_agent.py` | 516 | `SentimentAgent`, `analyze_sentiment` | `agents/analysis/` |
| `whale_agent.py` | 679 | `WhaleAgent`, `track_whales`, `alert_whale` | `agents/analysis/` |
| `funding_agent.py` | 527 | `FundingAgent`, `get_funding_rates` | `agents/analysis/` |
| `funding_agent_2.py` | 310 | Enhanced funding | Merge into funding_agent |
| `liquidation_agent.py` | 588 | `LiquidationAgent`, `track_liquidations` | `agents/analysis/` |
| `chartanalysis_agent.py` | 446 | `ChartAgent`, `analyze_chart` | `agents/analysis/` |
| `volume_agent.py` | 734 | `VolumeAgent`, `analyze_volume` | `agents/analysis/` |

#### Research Agents

| File | Lines | Key Classes/Functions | MoonView Target |
|------|-------|----------------------|-----------------|
| `rbi_agent.py` | 1,049 | `RBIAgent`, `research`, `backtest`, `implement` | `agents/research/` |
| `research_agent.py` | 569 | `ResearchAgent`, `web_research` | `agents/research/` |
| `backtest_runner.py` | ~200 | `run_backtest`, `analyze_results` | `agents/research/` |

#### Content Agents

| File | Lines | Key Classes/Functions | MoonView Target |
|------|-------|----------------------|-----------------|
| `chat_agent.py` | 653 | `ChatAgent`, `respond`, `maintain_context` | `agents/content/` |
| `clips_agent.py` | 668 | `ClipsAgent`, `create_clip`, `analyze_video` | `agents/content/` |
| `tweet_agent.py` | 270 | `TweetAgent`, `compose_tweet`, `post` | `agents/content/` |
| `video_agent.py` | 484 | `VideoAgent`, `create_video`, `edit` | `agents/content/` |
| `prompt_agent.py` | 510 | `PromptAgent`, `optimize_prompt` | `agents/content/` |

#### Data Agents

| File | Lines | Key Classes/Functions | MoonView Target |
|------|-------|----------------------|-----------------|
| `coingecko_agent.py` | 749 | `CoinGeckoAgent`, `get_market_data` | `agents/data/` |
| `polymarket_agent.py` | 1,485 | `PolymarketAgent`, `get_predictions` | `agents/data/` |
| `polymarket_websearch_agent.py` | 1,440 | Enhanced polymarket | `agents/data/` |
| `scraper_agent.py` | 685 | `ScraperAgent`, `scrape_url` | `agents/data/` |
| `websearch_agent.py` | 1,280 | `WebSearchAgent`, `search_web` | `agents/data/` |
| `focus_agent.py` | 542 | `FocusAgent` | `agents/data/` |
| `new_or_top_agent.py` | 543 | `TokenDiscoveryAgent` | `agents/data/` |

#### Specialized Agents

| File | Lines | Key Classes/Functions | MoonView Target |
|------|-------|----------------------|-----------------|
| `sniper_agent.py` | 337 | `SniperAgent`, `snipe_token` | `agents/specialized/` |
| `solana_agent.py` | 364 | `SolanaAgent`, `analyze_token` | `agents/specialized/` |
| `million_agent.py` | ~300 | `MillionAgent` | `agents/specialized/` |
| `tx_agent.py` | 273 | `TxAgent`, `analyze_tx` | `agents/specialized/` |
| `compliance_agent.py` | 503 | `ComplianceAgent` | `agents/specialized/` |
| `giveaway_agent.py` | 339 | `GiveawayAgent` | `agents/specialized/` |
| `housecoin_agent.py` | 615 | `HousecoinAgent` | `agents/specialized/` |
| `listingarb_agent.py` | 762 | `ListingArbAgent` | `agents/specialized/` |
| `fundingarb_agent.py` | 354 | `FundingArbAgent` | `agents/specialized/` |

#### Deprecated/Skip

| File | Lines | Reason |
|------|-------|--------|
| `chat_agent_ad.py` | 1,018 | Old version |
| `chat_agent_og.py` | 1,111 | Old version |
| `chat_question_generator.py` | 228 | Utility |
| `clean_ideas.py` | 280 | Script |
| `code_runner_agent.py` | 941 | Security |
| `demo_countdown.py` | ~100 | Demo |
| `example_unified_agent.py` | 217 | Template |
| `phone_agent.py` | 797 | Hardware |
| `rbi_agent_pp.py` | 1,313 | Superseded |
| `rbi_agent_pp_multi.py` | 1,838 | Superseded |
| `rbi_agent_v2.py` | 874 | Superseded |
| `rbi_agent_v2_simple.py` | 313 | Superseded |
| `rbi_agent_v3.py` | 1,167 | Evaluate |
| `rbi_batch_backtester.py` | 316 | Merge |
| `realtime_clips_agent.py` | 875 | Merge |
| `shortvid_agent.py` | 287 | Merge |
| `stream_agent.py` | 289 | Unclear |
| `swarm_agent.py` | 571 | Experimental |
| `tiktok_agent.py` | 1,288 | Platform |

---

## Function Duplication Report

### Critical Duplications Within This Project

| Function | Occurrences | Files | Resolution |
|----------|-------------|-------|------------|
| `market_buy()` | 4 | nice_funcs*.py | Create exchange-agnostic interface |
| `market_sell()` | 4 | nice_funcs*.py | Create exchange-agnostic interface |
| `get_position()` | 4 | nice_funcs*.py | Create exchange-agnostic interface |
| `close_position()` | 4 | nice_funcs*.py | Create exchange-agnostic interface |
| `chunk_kill()` | 3 | nice_funcs*.py | Single implementation |
| `pnl_close()` | 3 | nice_funcs*.py | Single implementation |
| `cancel_all_orders()` | 4 | nice_funcs*.py | Create exchange-agnostic interface |
| `limit_order()` | 3 | nice_funcs*.py | Create exchange-agnostic interface |
| `ask_bid()` | 2 | nice_funcs*.py | Single implementation |
| `get_data()` | 3 | nice_funcs*.py | Unify data fetching |
| `ai_entry()` | 2 | nice_funcs*.py | Single implementation |

### Pattern Analysis

The nice_funcs*.py files follow a pattern where each exchange has its own implementation:

```
nice_funcs.py           → Solana (Jupiter DEX)
nice_funcs_hyperliquid.py → HyperLiquid perps
nice_funcs_extended.py  → X10 exchange
nice_funcs_aster.py     → Aster exchange
```

**Recommended Resolution:**
Create an exchange-agnostic interface in moonview:

```python
# moonview.trading.orders
class OrderManager:
    def __init__(self, exchange: str):
        self.exchange = ExchangeFactory.create(exchange)

    def market_buy(self, symbol, amount, **kwargs):
        return self.exchange.market_buy(symbol, amount, **kwargs)

# moonview.api.exchanges
class ExchangeFactory:
    @staticmethod
    def create(exchange_name: str) -> BaseExchange:
        exchanges = {
            'solana': SolanaExchange,
            'hyperliquid': HyperliquidExchange,
            'x10': X10Exchange,
            'aster': AsterExchange,
        }
        return exchanges[exchange_name]()
```

---

## MoonView Overlap Analysis

### Functions That Already Exist in MoonView

| Function | moon-dev-ai-agents | MoonView Location | Action |
|----------|-------------------|-------------------|--------|
| `ask_bid()` | nice_funcs_hl.py | utils/trading/market_data.py | Use moonview |
| `get_position()` | nice_funcs*.py | utils/trading/positions.py | Use moonview |
| `calculate_rsi()` | Various | utils/indicators/momentum.py | Use moonview |
| `calculate_sma()` | Various | utils/indicators/trend.py | Use moonview |
| `calculate_ema()` | Various | utils/indicators/trend.py | Use moonview |
| `calculate_atr()` | Various | utils/indicators/volatility.py | Use moonview |
| `calculate_bollinger_bands()` | Various | utils/indicators/volatility.py | Use moonview |
| `calculate_macd()` | Various | utils/indicators/trend.py | Use moonview |
| `get_db_connection()` | Agents | utils/db/connection.py | Use moonview |
| `format_number()` | Various | utils/config_utils/formatters.py | Use moonview |

### Functions to Migrate (Don't Exist in MoonView)

| Function | Source | MoonView Target |
|----------|--------|-----------------|
| `token_overview()` | nice_funcs.py | moonview.api.blockchain.solana |
| `token_price()` | nice_funcs.py | moonview.api.blockchain.solana |
| `token_security_info()` | nice_funcs.py | moonview.api.blockchain.solana |
| `supply_demand_zones()` | nice_funcs.py | moonview.trading.signals |
| `elegant_entry()` | nice_funcs.py | moonview.trading.signals |
| `breakout_entry()` | nice_funcs.py | moonview.trading.signals |
| `ai_entry()` | nice_funcs*.py | moonview.trading.signals |
| `ModelFactory` | models/ | models/model_factory.py |
| `MoonDevAPI` | agents/api.py | moonview.api.moondev |

### Classes That Don't Exist in MoonView

| Class | Source | MoonView Target |
|-------|--------|-----------------|
| `ModelFactory` | models/model_factory.py | models/model_factory.py |
| `BaseModel` | models/base_model.py | models/base_model.py |
| `ClaudeModel` | models/claude_model.py | models/providers/claude.py |
| `OpenAIModel` | models/openai_model.py | models/providers/openai.py |
| `DeepSeekModel` | models/deepseek_model.py | models/providers/deepseek.py |
| `GroqModel` | models/groq_model.py | models/providers/groq.py |
| `GeminiModel` | models/gemini_model.py | models/providers/gemini.py |
| `OllamaModel` | models/ollama_model.py | models/providers/ollama.py |
| `OpenRouterModel` | models/openrouter_model.py | models/providers/openrouter.py |
| `XAIModel` | models/xai_model.py | models/providers/xai.py |
| `TokenTracker` | models/token_tracker.py | models/utils/token_tracker.py |
| `ExtendedExchangeAPI` | nice_funcs_extended.py | moonview.api.exchanges.x10 |

---

## Migration Decision Matrix

### Decision Categories

| Decision | Meaning |
|----------|---------|
| **MIGRATE** | Copy/adapt to moonview |
| **MERGE** | Combine with existing moonview code |
| **USE_MOONVIEW** | Use existing moonview implementation |
| **SKIP** | Don't migrate (deprecated, experimental) |
| **KEEP_HERE** | Keep in moon-dev-ai-agents (training, reference) |

### File Decisions

| File/Folder | Decision | Notes |
|-------------|----------|-------|
| `src/models/` | MIGRATE | All 12 files, moonview doesn't have LLM abstraction |
| `src/agents/api.py` | MERGE | MoonDevAPI exists partially in moonview |
| `src/agents/trading_agent.py` | MIGRATE | Core agent |
| `src/agents/risk_agent.py` | MIGRATE | Core agent |
| `src/agents/strategy_agent.py` | MIGRATE | Core agent |
| `src/agents/sentiment_agent.py` | MIGRATE | Analysis agent |
| `src/agents/whale_agent.py` | MIGRATE | Analysis agent |
| `src/agents/rbi_agent.py` | MIGRATE | Research agent |
| `src/agents/chat_agent.py` | MIGRATE | Content agent |
| `src/agents/chat_agent_og.py` | SKIP | Deprecated |
| `src/agents/swarm_agent.py` | SKIP | Experimental |
| `src/nice_funcs.py` | DECOMPOSE | Split to moonview modules |
| `src/nice_funcs_hyperliquid.py` | MERGE | Into moonview.api.exchanges.hyperliquid |
| `src/config.py` | MERGE | Into moonview config modules |
| `ATC Bootcamp Code 2025/` | KEEP_HERE | Training materials |

---

## Proposed Target Structure

### In MoonView After Migration

```
moonview/
├── models/                        # FROM moon-dev-ai-agents/src/models/
│   ├── __init__.py
│   ├── model_factory.py
│   ├── base_model.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── claude.py
│   │   ├── openai.py
│   │   ├── deepseek.py
│   │   ├── groq.py
│   │   ├── gemini.py
│   │   ├── ollama.py
│   │   ├── openrouter.py
│   │   └── xai.py
│   └── utils/
│       └── token_tracker.py
│
├── agents/                        # FROM moon-dev-ai-agents/src/agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── api.py                     # MoonDevAPI
│   ├── orchestrator.py            # FROM main.py
│   │
│   ├── trading/
│   │   ├── __init__.py
│   │   ├── trading_agent.py
│   │   ├── risk_agent.py
│   │   ├── strategy_agent.py
│   │   └── copybot_agent.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── sentiment_agent.py
│   │   ├── whale_agent.py
│   │   ├── funding_agent.py
│   │   ├── liquidation_agent.py
│   │   ├── chartanalysis_agent.py
│   │   └── volume_agent.py
│   │
│   ├── research/
│   │   ├── __init__.py
│   │   ├── rbi_agent.py
│   │   ├── research_agent.py
│   │   └── backtest_runner.py
│   │
│   ├── content/
│   │   ├── __init__.py
│   │   ├── chat_agent.py
│   │   ├── clips_agent.py
│   │   ├── tweet_agent.py
│   │   ├── video_agent.py
│   │   └── prompt_agent.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── coingecko_agent.py
│   │   ├── polymarket_agent.py
│   │   ├── scraper_agent.py
│   │   ├── websearch_agent.py
│   │   └── token_discovery_agent.py
│   │
│   └── specialized/
│       ├── __init__.py
│       ├── sniper_agent.py
│       ├── solana_agent.py
│       ├── tx_agent.py
│       └── arbitrage_agent.py     # Merged listingarb + fundingarb
│
└── src/moonview/
    ├── api/
    │   ├── exchanges/
    │   │   ├── solana.py          # FROM nice_funcs.py (Jupiter)
    │   │   ├── hyperliquid.py     # MERGE nice_funcs_hyperliquid.py
    │   │   ├── x10.py             # FROM nice_funcs_extended.py
    │   │   └── aster.py           # FROM nice_funcs_aster.py
    │   ├── blockchain/
    │   │   └── solana.py          # token_overview, token_price, etc.
    │   └── moondev.py             # MERGE with existing
    │
    └── trading/
        ├── signals.py             # supply_demand_zones, elegant_entry, etc.
        └── (existing files enhanced)
```

---

## Related Documentation

- `PROJECT_DOCUMENTATION.md` - Comprehensive project docs
- `MOONVIEW_TRANSITION.md` - Migration guide overview
- `~/WorkLocal/moonview/docs/MIGRATION_PLAN.md` - Master migration plan
- `~/WorkLocal/moonview/docs/AGENT_MIGRATION_CHECKLIST.md` - Agent tracking
- `~/WorkLocal/moonview/docs/MODELS_MIGRATION_GUIDE.md` - LLM layer migration
