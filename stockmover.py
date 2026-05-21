"""
Stock Mover - a daily Indian stock movement alerter.
Run with: python3 stockmover.py
"""

import json
import os
from datetime import date

import yfinance as yf

HISTORY_FILE = "history.json"

def load_history():
    """Read history.json from disk, or return an empty dict if it doesn't exist yet."""
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)
    
def save_history(history):
    """Wrote the history dict to disk as JSON."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


tickers = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
]

print("Loading history...")
history = load_history()
print(f"Hisory contains {len(history)} tickers. \n")

print("Fetching latest closes...")
today_str = date.today().isoformat()

for ticker_symbol in tickers:
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="2d")
    latest_close = data["Close"].iloc[-1]
    
    # Look up previous close from history, if available
    previous_entries = history.get(ticker_symbol, [])
    if previous_entries:
        previous_close = previous_entries[-1]["close"]
        percent_change = ((latest_close - previous_close) / previous_close) * 100
        print(f" {ticker_symbol:<15} {latest_close:>10.2f} -> {latest_close:>10.2f} ({percent_change:+.2f}%)")
    else:
        print(f" {ticker_symbol:<15} {latest_close:>10.2f} (no previous data)")

    # Add today's close to history
    if ticker_symbol not in history:
        history[ticker_symbol] = []
    
    today_entry = {"date": today_str, "close": round(float(latest_close), 2)}
    
    # If the last entry is today's, replace it. Otherwise append.
    if history[ticker_symbol] and history[ticker_symbol][-1]["date"] == today_str:
        history[ticker_symbol][-1] = today_entry
    else:
        history[ticker_symbol].append(today_entry)

print("\nSaving history...")
save_history(history)
print("\nDone")
