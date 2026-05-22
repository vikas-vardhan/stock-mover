# Stock Mover Project

## What this is
A Python script that checks a list of Indian stocks once daily and reports any that moved more than a configurable threshold (default 3%) since the previous run.

## How to use it

```
source venv/bin/activate
python3 stockmover.py
```

## Current state (as of Day 8)
Project scaffolded. No real logic yet — currently just prints a placeholder. Real implementation begins Day 9.

## Current state (as of Day 9)
Fetches latest closing prices for 8-stock watchlist via yfinance.
Watchlist still hardcoded in script; will move to config.json on Day 12.
No history comparison or alerts yet.

## Current state (as of Day 10)
- Fetches latest closing prices for 8-stock watchlist
- Persists price data to `history.json` between runs
- Compares today's close to most recent prior close
- Calculates percentage change (no alert threshold yet)
- Handles same-day re-runs without polluting history

## Current state (as of Day 11)
- Fetches latest closing prices for 8-stock watchlist
- Persists price data to `history.json` between runs
- Compares today's close to previous (pre-today) close
- Applies configurable threshold (currently 3%) to identify meaningful moves
- Outputs a formatted daily report with alerts, non-alerts, and missing-data sections
- Code organized into named functions for clarity and future extension

## Architecture
- `stockmover.py` — main script (single file for now)
- `config.json` — tickers, threshold, and other settings
- `history.json` — persistent state, tracks previous closes (gitignored)
- `alerts.log` — record of past alerts (gitignored)
- `.env` — email credentials (gitignored, Day 13+)
- `requirements.txt` — Python dependencies

## Conventions
- Python 3, virtual environment in `venv/`
- All config externalized to `config.json`, no magic values in code
- Standard library + minimal third-party packages
- All secrets in `.env`, never committed
- Errors handled gracefully — tool should never crash on network issues

## Planned features (in build order)
- [x] Fetch real prices via yfinance (Day 9)
- [x] Persist price history (Day 10)
- [x] Alert logic with threshold (Day 11)
- [ ] CLI args for overriding config (Day 12)
- [ ] Email alerts (Day 13, stretch)

## What Claude Code should know
- The user is learning Python alongside this project
- Prefer simple, readable code over clever shortcuts
- Always explain before changing files
- Git operations are done manually by the user, not from inside Claude Code

