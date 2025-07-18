#!/usr/bin/env python3.13
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
from pendulum import DateTime, now
from yfinance import download


def main() -> None:
  tickers: tuple[str, ...] = ("tsla", "msft")
  end_time: DateTime = now(tz="UTC")
  start_time: DateTime = end_time.subtract(days=30)
  data: list[DataFrame] = [
    DataFrame(
      download(
        ticker,
        auto_adjust=True,
        end=end_time.format("YYYY-MM-DD"),
        multi_level_index=False,
        start=start_time.format("YYYY-MM-DD"),
      )
    )
    for ticker in tickers
  ]
  concat(data).to_csv("data.csv")


if __name__ == "__main__":
  main()
