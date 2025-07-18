#!/usr/bin/env python3.13
# coding:utf-8
# Copyright (C) 2024-2025 All rights reserved.
# FILENAME:    ~~/src/polars_v_pandas/compare.py
# VERSION:     0.0.1
# CREATED:     2025-07-18 21:27
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from textwrap import dedent

### Local modules ###
from polars_v_pandas.utils import evaluate_and_show

R: int = 5  # Calls the timeit() repeatedly, returning a list of results
N: int = 10  # How many times to execute statement


def main() -> None:
  # --- Test 1 --- (Read a single CSV file)
  SETUP_PANDAS: str = """import pandas as pd"""
  SETUP_POLARS: str = """import polars as pl"""
  test_name = "Read a single CSV file"
  statement_pandas = """pd.read_csv("./data.csv", engine='pyarrow')"""
  statement_polars = """pl.read_csv("./data.csv")"""

  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pdc=SETUP_PANDAS,
    setup_pda=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )

  # --- Test 2 --- (Selecting v1)
  test_name = "Selecting columns (v1)"
  SETUP_PANDAS = dedent("""
  import pandas as pd
  df_pandas = pd.read_csv('./data.csv')
  """)
  SETUP_PANDAS_C = dedent("""
  import pandas as pd
  df_pandas = pd.read_csv('./data.csv', engine='c')
  """)
  SETUP_PANDAS_PYARROW = dedent("""
  import pandas as pd
  df_pandas = pd.read_csv('./data.csv', engine='pyarrow')
  """)
  SETUP_POLARS = dedent("""
  import polars as pl
  df_polars = pl.read_csv('./data.csv')
  """)

  statement_pandas = """df_pandas[['Open', 'High']]"""
  statement_polars = """df_polars[['Open', 'High']]"""
  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    setup_pdc=SETUP_PANDAS_C,
    setup_pda=SETUP_PANDAS_PYARROW,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )

  # --- Test 3 --- (Selecting v2)
  test_name = "Selecting columns (v2)"
  statement_pandas = """df_pandas[['Date', 'Volume']]"""
  statement_polars = """df_polars.select(['Date', 'Volume'])"""
  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    setup_pdc=SETUP_PANDAS_C,
    setup_pda=SETUP_PANDAS_PYARROW,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )

  # --- Test 4 --- (Filtering)
  test_name = "Filtering"
  statement_pandas = """df_pandas.query('Low > 5')"""
  statement_polars = """df_polars.filter(pl.col('Low') > 5)"""
  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    setup_pdc=SETUP_PANDAS_C,
    setup_pda=SETUP_PANDAS_PYARROW,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )

  # --- Test 5 --- (Create a new Column v1)
  test_name = "Create a new column (v1)"
  statement_pandas = """df_pandas['new_col'] = df_pandas['Low'] * 10"""
  statement_polars = """df_polars.with_columns((pl.col('Low') * 10).alias('new_col'))"""
  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    setup_pdc=SETUP_PANDAS_C,
    setup_pda=SETUP_PANDAS_PYARROW,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )

  # --- Test 6 --- (Creating new Columns v2)
  test_name = "Create a new column (v2)"
  statement_pandas = """df_pandas['new_col'] = df_pandas['Low'] * 10"""
  statement_polars = """df_polars.lazy().with_columns((pl.col('Low') * 10).alias('new_col'))"""
  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    setup_pdc=SETUP_PANDAS_C,
    setup_pda=SETUP_PANDAS_PYARROW,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )

  # --- Test 7 --- (Group and aggregate)
  test_name = "Group and aggregate"
  statement_pandas = """df_pandas.groupby('Low')['Close'].agg('mean')"""
  statement_polars = """df_polars.group_by('Low').agg([pl.mean('Close')])"""  # shorter
  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    setup_pdc=SETUP_PANDAS_C,
    setup_pda=SETUP_PANDAS_PYARROW,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )

  # --- Test 8 --- (Missing data)
  test_name = "Fill missing data"
  statement_pandas = """df_pandas['Close'].fillna(-999)"""
  statement_polars = """df_polars.with_columns(pl.col('Close').fill_null(-999))"""
  evaluate_and_show(
    setup_pd=SETUP_PANDAS,
    setup_pl=SETUP_POLARS,
    setup_pdc=SETUP_PANDAS_C,
    setup_pda=SETUP_PANDAS_PYARROW,
    stmt_pd=statement_pandas,
    stmt_pl=statement_polars,
    R=R,
    N=N,
    test_name=test_name,
  )


if __name__ == "__main__":
  main()


__all__: tuple[str, ...] = ("main",)
