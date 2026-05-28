# Stock Mover - Project Specification

## What this is
This prject is to highlight and notify me about any big moves in the share price of the companies specified by me.

## Why I.m buildnig it
It will help me to look into these companies for any specific reasons that caused the moves and act accordingly, if needed.

## What it does
It checks the close share price of the companies in my watchlist.
It refers to yahoo finance for now to check if the share price has changed more than +/- 3 per cent
It triggers an email to me regarding the same.

## What it doesn't do
It does not gives me any qualitative information about the company.

## Inputs
 - A config file with tickers and threshold
 - (Eventually) email credentials in a .env file

## Outputs
 - Formatted termial output showing alerts and non-alerts
 - (Eventually) email when the alerts are present
 - A history.json file that builds up over time

## Success criteria
I get timely alert and it is able to give me the actual changes in the stock prices from Yahoo Finance

## What I exoect to learn]
Creating a small problem solving project end-to-end using python and libraries.

## Open Questions
I wil note them down as the project preogresses.

## Design decisions
- Daily comparison uses market data's previous trading day (iloc[-2]),
  not the history file. This keeps results correct even if the tool is
  run irregularly. History is a record, not the comparison source.
