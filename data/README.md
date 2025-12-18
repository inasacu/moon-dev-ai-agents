# Data Folder Structure

**Synced from:** `~/WorkLocal/moonview/data/`
**Last Updated:** 2025-12-18

This folder mirrors the MoonView project's data organization for consistency across both projects.

---

## Folder Structure

```
data/
├── archive/              # Historical/archived data
│   ├── csv/             # Archived CSV exports
│   ├── results/         # Archived analysis results
│   └── whales/          # Archived whale tracking data
│
├── raw/                  # Raw, unprocessed data
│   ├── csv/             # Raw CSV data files
│   ├── html/            # Scraped HTML content
│   ├── txt/             # Raw text files
│   ├── results/         # Raw analysis outputs
│   ├── reports/         # Generated reports
│   ├── whales/          # Whale activity tracking
│   │
│   └── rbi/             # Research-Backtest-Implement data
│       ├── strategies/  # Strategy definitions
│       ├── bt_code/     # Backtest code generated
│       ├── ids/         # Strategy/backtest IDs
│       ├── results/     # Backtest results
│       └── data/        # OHLCV and market data for backtests
│
├── oi_total.csv         # Open Interest totals (runtime)
└── open_interest.csv    # Detailed OI data (runtime)
```

---

## Usage Guidelines

### Archive vs Raw
- **`raw/`**: Active working data, frequently updated
- **`archive/`**: Completed analyses, historical snapshots (rarely modified)

### RBI (Research-Backtest-Implement) Workflow
1. **`strategies/`**: Store strategy logic definitions (YAML/JSON/Python)
2. **`bt_code/`**: AI-generated backtest code from RBI agent
3. **`ids/`**: Track strategy/backtest run identifiers
4. **`results/`**: Backtest performance metrics and reports
5. **`data/`**: OHLCV data used for backtesting

### File Naming Conventions
- CSVs: `{symbol}_{timeframe}_{rows}.csv` (e.g., `BTC-USD_1h_5000.csv`)
- Results: `{strategy}_{date}_{id}.json`
- Reports: `report_{type}_{date}.html`

---

## Git Tracking

This folder structure is tracked via `.gitkeep` files.
**Actual data files are gitignored** to prevent large files and sensitive data from being committed.

To sync data between projects, use rsync or manual copy:
```bash
# Sync from moonview to moon-dev-ai-agents
rsync -av ~/WorkLocal/moonview/data/ ~/WorkLocal/moon-dev-ai-agents/data/
```

---

## Related Folders

- **`src/data/`**: Agent-specific data outputs (tracked separately)
- **`mean reversion june 21/`**: Strategy-specific OHLCV data
