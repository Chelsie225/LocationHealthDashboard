from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

# CDC PLACES county dataset CSV download endpoint (Socrata)
PLACES_COUNTY_CSV = "https://data.cdc.gov/api/views/swc5-untb/rows.csv?accessType=DOWNLOAD"


@st.cache_data(show_spinner="Downloading CDC PLACES county data… (first run only)")
def load_places_county(limit_rows: int | None = None) -> pd.DataFrame:
    """
    Downloads CDC PLACES county-level data as a DataFrame.
    Uses Streamlit caching to avoid repeated downloads.
    """
    r = requests.get(PLACES_COUNTY_CSV, timeout=60)
    r.raise_for_status()

    df = pd.read_csv(pd.io.common.BytesIO(r.content))

    if limit_rows is not None:
        df = df.head(limit_rows)

    # Normalize some common column names across exports
    rename_map = {
        "StateAbbr": "state",
        "StateDesc": "state_name",
        "CountyName": "county",
        "LocationName": "location_name",
        "Measure": "measure",
        "MeasureId": "measure_id",
        "Category": "category",
        "DataValue": "value",
        "DataValueUnit": "unit",
        "DataValueType": "value_type",
        "Year": "year",
    }
    for k, v in rename_map.items():
        if k in df.columns and v not in df.columns:
            df = df.rename(columns={k: v})

    essentials = [c for c in ["state", "county", "measure", "value"] if c in df.columns]
    if essentials:
        df = df.dropna(subset=essentials)

    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    return df


def available_states(df: pd.DataFrame) -> list[str]:
    if "state" not in df.columns:
        return []
    return sorted([s for s in df["state"].dropna().unique().tolist()])


def available_measures(df: pd.DataFrame) -> list[str]:
    if "measure" not in df.columns:
        return []
    return sorted([m for m in df["measure"].dropna().unique().tolist()])
