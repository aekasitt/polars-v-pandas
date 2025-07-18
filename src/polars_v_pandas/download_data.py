#!/usr/bin/env python3

import pandas as pd
import yfinance as yf


tickers = ["tsla", "msft"]

ticker_list = [pd.DataFrame(yf.download(ticker, start="2024-01-01", end="2024-02-26")) for ticker in tickers]
pd.concat(ticker_list).to_csv("data.csv")

