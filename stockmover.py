"""
Stock Mover - a daily Indian stock movement alerter.
Run with: python3 stockmover.py
"""

import yfinance as yf

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

print(f"Fetching latest closes for watchlist...\n")

for ticker_symbol in tickers:
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="2d")
    latest_close = data["Close"].iloc[-1]
    print(f" {ticker_symbol:<15} {latest_close:>10.2f}")

print("\nDone")
