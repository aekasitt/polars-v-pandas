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

### Third-party packages ###
import numpy as np

### Local modules ###
from polars_v_pandas.utils import (
    # test_it,                 # execute a given function
    show_results,            # show results in terminal
    show_graph,              # show results in chart
    evaluate_and_show        # orchestrate whole output mechanism
)

# Experiment parameters
R = 5   # Calls the timeit() repeatedly, returning a list of results
N = 10  # How many times to execute statement

# SETUP_PANDAS = '''import pandas as pd'''
# SETUP_POLARS = '''import polars as pl'''

if __name__ == "__main__":
  # --- Test 1 --- (Read a single CSV file)
  # test_name = 'Read a single CSV file'
  # statement_pandas = '''pd.read_csv("./data.csv", engine='pyarrow')'''
  # statement_polars = '''pl.read_csv("./data.csv")'''
  
  # t_pandas = test_it(setup=SETUP_PANDAS, statement=statement_pandas, R=R, N=N)
  # t_polars = test_it(setup=SETUP_POLARS, statement=statement_polars, R=R, N=N)
  # evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
  #                   stmt_pd=statement_pandas, stmt_pl=statement_polars,
  #                   R=R, N=N, test_name=test_name)
  
  
  # --- Test 2 --- (Selecting v1)
  test_name = 'Selecting columns (v1)'
  SETUP_PANDAS = '''
  import pandas as pd
  df_pandas = pd.read_csv('./data.csv')
  '''
  SETUP_PANDAS_C = '''
  import pandas as pd
  df_pandas = pd.read_csv('./data.csv', engine='c')
  '''
  SETUP_PANDAS_PYARROW = '''
  import pandas as pd
  df_pandas = pd.read_csv('./data.csv', engine='pyarrow')
  '''
  SETUP_POLARS = '''
  import polars as pl
  df_polars = pl.read_csv('./data.csv')
  '''
  
  statement_pandas = '''df_pandas[['Open', 'High']]'''
  statement_polars = '''df_polars[['Open', 'High']]'''
  evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
                    setup_pdc=SETUP_PANDAS_C, setup_pda=SETUP_PANDAS_PYARROW,
                    stmt_pd=statement_pandas, stmt_pl=statement_polars,
                    R=R, N=N, test_name=test_name)
  
  
  # --- Test 3 --- (Selecting v2)
  test_name = 'Selecting columns (v2)'
  statement_pandas = '''df_pandas[['Date', 'Volume']]'''
  statement_polars = '''df_polars.select(['Date', 'Volume'])'''
  evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
                    setup_pdc=SETUP_PANDAS_C, setup_pda=SETUP_PANDAS_PYARROW,
                    stmt_pd=statement_pandas, stmt_pl=statement_polars,
                    R=R, N=N, test_name=test_name)
  
  
  # --- Test 4 --- (Filtering)
  test_name = 'Filtering'
  statement_pandas = '''df_pandas.query('Low > 5')'''
  statement_polars = '''df_polars.filter(pl.col('Low') > 5)'''
  evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
                    setup_pdc=SETUP_PANDAS_C, setup_pda=SETUP_PANDAS_PYARROW,
                    stmt_pd=statement_pandas, stmt_pl=statement_polars,
                    R=R, N=N, test_name=test_name)
  
  
  # --- Test 5 --- (Create a new Column v1)
  test_name = 'Create a new column (v1)'
  statement_pandas = '''df_pandas['new_col'] = df_pandas['Low'] * 10'''
  statement_polars = '''df_polars.with_columns((pl.col('Low') * 10).alias('new_col'))'''
  evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
                    setup_pdc=SETUP_PANDAS_C, setup_pda=SETUP_PANDAS_PYARROW,
                    stmt_pd=statement_pandas, stmt_pl=statement_polars,
                    R=R, N=N, test_name=test_name)
  
  
  # --- Test 6 --- (Creating new Columns v2)
  test_name = 'Create a new column (v2)'
  statement_pandas = '''df_pandas['new_col'] = df_pandas['Low'] * 10'''
  statement_polars = '''df_polars.lazy().with_columns((pl.col('Low') * 10).alias('new_col'))'''
  evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
                    setup_pdc=SETUP_PANDAS_C, setup_pda=SETUP_PANDAS_PYARROW,
                    stmt_pd=statement_pandas, stmt_pl=statement_polars,
                    R=R, N=N, test_name=test_name)
  
  
  # --- Test 7 --- (Group and aggregate)
  test_name = 'Group and aggregate'
  statement_pandas = '''df_pandas.groupby('Low')['Close'].agg('mean')'''
  statement_polars = '''df_polars.groupby('Low').agg([pl.mean('Close')])'''  # shorter
  evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
                    setup_pdc=SETUP_PANDAS_C, setup_pda=SETUP_PANDAS_PYARROW,
                    stmt_pd=statement_pandas, stmt_pl=statement_polars,
                    R=R, N=N, test_name=test_name)
  
  
  # --- Test 8 --- (Missing data)
  test_name = 'Fill missing data'
  statement_pandas = '''df_pandas['Close'].fillna(-999)'''
  statement_polars = '''df_polars.with_columns(pl.col('Close').fill_null(-999))'''
  evaluate_and_show(setup_pd=SETUP_PANDAS, setup_pl=SETUP_POLARS,
                    setup_pdc=SETUP_PANDAS_C, setup_pda=SETUP_PANDAS_PYARROW,
                    stmt_pd=statement_pandas, stmt_pl=statement_polars,
                    R=R, N=N, test_name=test_name)
