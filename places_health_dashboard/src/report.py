from __future__ import annotations

from datetime import datetime
import pandas as pd


def make_rank_tables(df: pd.DataFrame, group_col: str, value_col: str, n: int = 10):
    """
    Returns (top_n_df, bottom_n_df) with [group_col, value_col], sorted for readability.
    """
    d = df[[group_col, value_col]].dropna().copy()
    d = d.sort_values(value_col)

    bottom = d.head(n).reset_index(drop=True)
    top = d.tail(n).sort_values(value_col, ascending=False).reset_index(drop=True)

    return top, bottom


def build_markdown_report(
    state: str,
    measure: str,
    year: int | None,
    top_df: pd.DataFrame,
    bottom_df: pd.DataFrame,
    notes: str = "",
) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    year_line = f"**Year:** {year}\n" if year is not None else "**Year:** All available\n"

    md = f"""# PLACES Auto-Report

**State:** {state}  
**Measure:** {measure}  
{year_line}
**Generated:** {ts}

## Summary
This report ranks counties by the selected PLACES measure. Use it to quickly identify places with the highest and lowest estimates, then follow up with local context, uncertainty, and additional indicators.

## Top 10 Counties (Highest Values)
{top_df.to_markdown(index=False)}

## Bottom 10 Counties (Lowest Values)
{bottom_df.to_markdown(index=False)}

## Notes / Interpretation
{notes if notes.strip() else "- (Add your interpretation here — what patterns do you notice? What would you investigate next?)"}

## Limitations
- PLACES provides model-based estimates; values may include uncertainty.
- Rankings can change based on year availability, missing data, and measure definitions.
- Pair this report with other sources and local context before making decisions.
"""
    return md


def safe_filename(text: str) -> str:
    keep = []
    for ch in text:
        if ch.isalnum() or ch in ("-", "_"):
            keep.append(ch)
        elif ch in (" ", "/"):
            keep.append("_")
    out = "".join(keep).strip("_")
    return out[:80] if len(out) > 80 else out
