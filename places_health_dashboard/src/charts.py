from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def bar_top_bottom(df: pd.DataFrame, group_col: str, value_col: str, n: int = 10):
    """
    Creates a figure with Bottom N and Top N horizontal bar charts.
    """
    d = df[[group_col, value_col]].dropna().copy()
    d = d.sort_values(value_col)

    bottom = d.head(n)
    top = d.tail(n)

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    ax1.barh(bottom[group_col].astype(str), bottom[value_col])
    ax1.set_title(f"Bottom {n}")
    ax1.invert_yaxis()

    ax2.barh(top[group_col].astype(str), top[value_col])
    ax2.set_title(f"Top {n}")
    ax2.invert_yaxis()

    fig.tight_layout()
    return fig


def line_over_time(df: pd.DataFrame, x_col: str, y_col: str):
    """
    Creates a simple line chart over time.
    """
    d = df[[x_col, y_col]].dropna().copy().sort_values(x_col)

    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(d[x_col], d[y_col], marker="o")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title("Trend over time")
    fig.tight_layout()
    return fig
