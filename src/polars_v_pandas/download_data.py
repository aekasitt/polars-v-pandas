#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2024-2025 All rights reserved.
# FILENAME:    ~~/src/polars_v_pandas/download_data.py
# VERSION:     0.0.1
# CREATED:     2025-07-18 21:27
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pandas import DataFrame, concat
from yfinance import download


def main() -> None:
  tickers: tuple[str, ...] = ("tsla", "msft")
  data: list[DataFrame] = [
    DataFrame(download(ticker, start="2024-01-01", end="2024-02-26")) for ticker in tickers
  ]
  concat(data).to_csv("data.csv")


if __name__ == "__main__":
  main()
