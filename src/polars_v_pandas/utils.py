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
"""
This collections of functions and procedures supports the main testing script
test.py to compare Polars and Pandas modules. The following functions performs
calculation of average working duration, delivers results to terminal window
and display results on graphs.
"""

### Standard packages ###
import timeit
from operator import itemgetter

### Third-party packages ###
import numpy as np
from matplotlib import pyplot as plt

# Supporting functions
def test_it(setup: str, statement: str, R: int, N: int) -> list:
    """
    Test specific function and return durations in generated list.
    """

    t = timeit.repeat(setup=setup,
                      stmt=statement,
                      repeat=R,
                      number=N)
    return t


def show_results(dur_pd: list, dur_pdc : list, dur_pda : list, dur_pl : list, test_name : str) -> None:
    """
    Show results directly in terminal windows (average durations and standard
    deviation)
    """
    round_three = lambda n: np.round(n, 3)
    averages : list = list(map(np.mean, [dur_pd, dur_pdc, dur_pda, dur_pl]))
    rounded_averages : list = list(map(round_three, averages))
    stdevs : list = list(map(round_three, map(np.std, [dur_pd, dur_pdc, dur_pda, dur_pl])))
    max_index, max_value = max(enumerate(averages), key=itemgetter(1))
    min_index, min_value = min(enumerate(averages), key=itemgetter(1))
    winner : str = ("Pandas", "Pandas (c-engine)", "Pandas (pyarrow-engine)", "Polars")[max_index]
    loser : str = ("Pandas", "Pandas (c-engine)", "Pandas (pyarrow-engine)", "Polars")[min_index]

    print(f'| Test name: {test_name}')
    print(f'|   Average duration [Pandas]: {rounded_averages[0]}, Std: {stdevs[0]}')
    print(f'|   Average duration [Pandas (c-engine)]: {rounded_averages[1]}, Std: {stdevs[1]}')
    print(f'|   Average duration [Pandas (pyarrow-engine)]: {rounded_averages[2]}, Std: {stdevs[2]}')
    print(f'|   Average duration [Polars]: {rounded_averages[3]}, Std: {stdevs[3]}')
    print(f'|   --> {winner} is {np.round(max_value / min_value, 2)} times than the slowest ({loser}).')
    print('-'*10)

    return None


def show_graph(dur_pd : list, dur_pdc : list, dur_pda : list, dur_pl: list, text_name:str) -> None:
    """
    Showing a histogram representing duration of a given function to perform for
    both Pandas and Polar modules.
    """
    names = ['Pandas', 'Pandas (c-engine)', 'Pandas (pyarrow-engine)', 'Polar']
    avg_pd, avg_pdc, avg_pda, avg_pl = np.mean(dur_pd), np.mean(dur_pdc), np.mean(dur_pda), np.mean(dur_pl)
    _ = plt.bar(x=names[0], height=avg_pd,
                edgecolor='black',
                linewidth=5,
                alpha=0.8,
                fill=True,
                color=['#154c79'],
                label=f'{names[0]} = {np.round(np.mean(dur_pd), 2)} s')
    _ = plt.bar(x=names[1], height=avg_pdc,
                edgecolor='black',
                linewidth=5,
                alpha=0.8,
                fill=True,
                color=['#154c79'],
                label=f'{names[1]} = {np.round(np.mean(dur_pdc), 2)} s')
    _ = plt.bar(x=names[2], height=avg_pda,
                edgecolor='black',
                linewidth=5,
                alpha=0.8,
                fill=True,
                color=['#154c79'],
                label=f'{names[2]} = {np.round(np.mean(dur_pda), 2)} s')
    _ = plt.bar(x=names[3], height=avg_pl,
                edgecolor='black',
                linewidth=5,
                alpha=0.8,
                fill=True,
                color=['#4454c7'],
                label=f'{names[3]} = {np.round(np.mean(dur_pl), 2)} s')
    _ = plt.title(text_name, fontsize=12)
    _ = plt.grid(which='major', color='black', linestyle='--', alpha=0.5)
    _ = plt.xlabel('Python module', fontsize=11)
    _ = plt.ylabel('Duration [s]', fontsize=11)
    _ = plt.legend(shadow=True)
    plt.show()

    return None


def evaluate_and_show(setup_pd: str, setup_pdc : str, setup_pda : str, setup_pl : str,
                      stmt_pd: str, stmt_pl : str,
                      R: int, N: int, test_name: str) -> None:
    """
    Orchestrate statement evaluation and show results in terminal and in barchart.
    """
    t_pandas = test_it(setup=setup_pd, statement=stmt_pd, R=R, N=N)
    t_pandas_c = test_it(setup=setup_pdc, statement=stmt_pd, R=R, N=N)
    t_pandas_arrow = test_it(setup=setup_pda, statement=stmt_pd, R=R, N=N)
    t_polars = test_it(setup=setup_pl, statement=stmt_pl, R=R, N=N)
    show_results(dur_pd=t_pandas, dur_pdc=t_pandas_c, dur_pda=t_pandas_arrow, dur_pl=t_polars, test_name=test_name)
    show_graph(dur_pd=t_pandas, dur_pdc=t_pandas_c, dur_pda=t_pandas_arrow, dur_pl=t_polars, text_name=test_name)

    return None

__all__: tuple[str, ...] = ("evaluate_and_show", "show_result", "test_it")
