"""
Stock Mover — a daily Indian stock movement alerter.
Run with: python3 stockmover.py
"""

import json
import os
from datetime import datetime, date

import yfinance as yf

import argparse


HISTORY_FILE = "history.json"
CONFIG_FILE = "config.json"


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



def load_config():
    """
    Read config.json and return its contents.
    Falls back to sensible defaults if the file is missing,
    and exits with a clear message if the file exists but is broken.
    """
    defaults = {
        "tickers": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
        "threshold_percent": 3.0,
        "history_days_to_keep": 30,
    }
    
    if not os.path.exists(CONFIG_FILE):
        print(f"⚠️  {CONFIG_FILE} not found. Using built-in defaults.")
        return defaults
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: {CONFIG_FILE} is not valid JSON.")
        print(f"   Details: {e}")
        print(f"   Fix the file or delete it to use defaults.")
        raise SystemExit(1)
    
    # Fill in any missing keys with defaults
    for key, value in defaults.items():
        if key not in config:
            print(f"⚠️  '{key}' missing from config, using default: {value}")
            config[key] = value
    
    return config


def fetch_two_closes(ticker_symbol):
    """
    Fetch the previous trading day's close and the latest close
    for a single ticker. Requests a 5-day window for reliability
    (period='2d' can return only one row near holidays/weekends),
    then uses the most recent two rows.
    Returns a tuple: (previous_close, latest_close).
    Either value may be None if data is insufficient.
    """
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="5d")

    closes = data["Close"]

    if len(closes) == 0:
        return (None, None)
    elif len(closes) == 1:
        return (None, float(closes.iloc[-1]))
    else:
        return (float(closes.iloc[-2]), float(closes.iloc[-1]))


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


def print_header(threshold):
    """Print the report header banner."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("=" * 48)
    print("  Stock Mover — Daily Report")
    print(f"  Run time: {now}")
    print(f"  Threshold: ±{threshold}%")
    print("=" * 48)
    print()


def print_footer():
    """Print the report footer banner."""
    print("=" * 48)
    print("  Run complete. History updated.")
    print("=" * 48)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check Indian stocks for significant daily moves."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Override the alert threshold percentage (e.g. --threshold 5)",
    )
    return parser.parse_args()

def main():
    """Run one cycle: fetch prices, compare to history, print alerts, save state."""
    args = parse_args()
    config = load_config()
    tickers = config["tickers"]
    threshold = config["threshold_percent"]
    
    # Command-line threshold overrides config threshold if provided
    threshold = args.threshold if args.threshold is not None else config["threshold_percent"]

    print_header(threshold)
    
    history = load_history()
    today_str = date.today().isoformat()
    
    alerts = []
    quiet = []
    no_data = []
    
    for ticker_symbol in tickers:
        previous_close, latest_close = fetch_two_closes(ticker_symbol)
        
        if latest_close is None:
            no_data.append(ticker_symbol)
            continue  # skip to next ticker — nothing to record or compare
        
        if previous_close is None:
            # Have today's price but no previous to compare against
            no_data.append(ticker_symbol)
        else:
            change = percent_change(previous_close, latest_close)
            if abs(change) >= threshold:
                alerts.append(format_alert(ticker_symbol, previous_close, latest_close, change))
            else:
                quiet.append(ticker_symbol)
        
        # Still record today's close in history (for future trend features)
        update_history(history, ticker_symbol, today_str, latest_close)
    
    # Print alerts section
    if alerts:
        print(f"🔔 Alerts ({len(alerts)}):")
        for line in alerts:
            print(line)
        print()
    else:
        print(f"✓ No alerts today. All tickers within ±{threshold}%.")
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
