"""
Stock Mover — a daily Indian stock movement alerter.
Run with: python3 stockmover.py
"""

import json
import os
from datetime import datetime, date

import yfinance as yf


HISTORY_FILE = "history.json"
THRESHOLD_PERCENT = 1.0

TICKERS = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
]


def load_history():
    """Read history.json from disk, or return an empty dict if it doesn't exist yet."""
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    """Write the history dict to disk as JSON."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def fetch_latest_close(ticker_symbol):
    """Fetch the most recent closing price for a single ticker."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="2d")
    return float(data["Close"].iloc[-1])


def get_previous_close(history, ticker_symbol, today_str):
    """
    Return the most recent close BEFORE today for this ticker,
    or None if no prior data exists.
    """
    entries = history.get(ticker_symbol, [])
    # Walk backward through entries, skip any from today
    for entry in reversed(entries):
        if entry["date"] != today_str:
            return entry["close"]
    return None


def update_history(history, ticker_symbol, today_str, close):
    """Add or replace today's entry for this ticker."""
    if ticker_symbol not in history:
        history[ticker_symbol] = []
    
    today_entry = {"date": today_str, "close": round(close, 2)}
    
    # If the last entry is today's, replace it. Otherwise append.
    if history[ticker_symbol] and history[ticker_symbol][-1]["date"] == today_str:
        history[ticker_symbol][-1] = today_entry
    else:
        history[ticker_symbol].append(today_entry)


def percent_change(old_value, new_value):
    """Return the percentage change from old_value to new_value."""
    return ((new_value - old_value) / old_value) * 100


def format_alert(ticker_symbol, previous_close, latest_close, change):
    """Format a single alert line with direction arrow."""
    arrow = "↑" if change > 0 else "↓"
    return f"  {arrow} {ticker_symbol:<15} {previous_close:>10.2f} → {latest_close:>10.2f}  ({change:+.2f}%)"


def print_header():
    """Print the report header banner."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("=" * 48)
    print("  Stock Mover — Daily Report")
    print(f"  Run time: {now}")
    print(f"  Threshold: ±{THRESHOLD_PERCENT}%")
    print("=" * 48)
    print()


def print_footer():
    """Print the report footer banner."""
    print("=" * 48)
    print("  Run complete. History updated.")
    print("=" * 48)


def main():
    """Run one cycle: fetch prices, compare to history, print alerts, save state."""
    print_header()
    
    history = load_history()
    today_str = date.today().isoformat()
    
    alerts = []
    quiet = []
    no_data = []
    
    for ticker_symbol in TICKERS:
        latest_close = fetch_latest_close(ticker_symbol)
        previous_close = get_previous_close(history, ticker_symbol, today_str)
        
        if previous_close is None:
            no_data.append(ticker_symbol)
        else:
            change = percent_change(previous_close, latest_close)
            if abs(change) >= THRESHOLD_PERCENT:
                alerts.append(format_alert(ticker_symbol, previous_close, latest_close, change))
            else:
                quiet.append(ticker_symbol)
        
        update_history(history, ticker_symbol, today_str, latest_close)
    
    # Print alerts section
    if alerts:
        print(f"🔔 Alerts ({len(alerts)}):")
        for line in alerts:
            print(line)
        print()
    else:
        print(f"✓ No alerts today. All tickers within ±{THRESHOLD_PERCENT}%.")
        print()
    
    # Print quiet section
    if quiet:
        print(f"  No alerts ({len(quiet)}):")
        print(f"     {', '.join(quiet)}")
        print()
    
    # Print "no data" section if relevant
    if no_data:
        print(f"⚠️  No prior data for ({len(no_data)}):")
        print(f"     {', '.join(no_data)}")
        print("     (Today's prices saved — comparisons available tomorrow.)")
        print()
    
    save_history(history)
    print_footer()


if __name__ == "__main__":
    main()
