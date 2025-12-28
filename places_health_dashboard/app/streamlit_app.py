from __future__ import annotations

import os
import streamlit as st

from src.data import load_places_county, available_states, available_measures
from src.charts import bar_top_bottom, line_over_time
from src.report import make_rank_tables, build_markdown_report, safe_filename

st.set_page_config(
    page_title="PLACES Health Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 PLACES Public Health Dashboard")
st.caption("County-level health estimates (CDC PLACES). Filter and compare measures across counties.")

df = load_places_county()

# ---- Sidebar: filters
st.sidebar.header("Filters")

states = available_states(df)
measures = available_measures(df)

state_default_idx = states.index("PA") if "PA" in states else 0
state = st.sidebar.selectbox("State", options=states, index=state_default_idx)
measure = st.sidebar.selectbox("Measure", options=measures)

filtered = df.copy()
if "state" in filtered.columns:
    filtered = filtered[filtered["state"] == state]
if "measure" in filtered.columns:
    filtered = filtered[filtered["measure"] == measure]

# Optional year filter if year exists
year = None
if "year" in filtered.columns and filtered["year"].notna().any():
    years = sorted(filtered["year"].dropna().unique().tolist())
    picked = st.sidebar.selectbox("Year (if available)", options=["All"] + [int(y) for y in years])
    if picked != "All":
        year = int(picked)
        filtered = filtered[filtered["year"] == year]

# County picker (optional)
county = None
if "county" in filtered.columns:
    counties = sorted(filtered["county"].dropna().unique().tolist())
    county = st.sidebar.selectbox("County (optional)", options=["All"] + counties)

county_view = filtered
if county and county != "All" and "county" in filtered.columns:
    county_view = filtered[filtered["county"] == county]

# ---- Main content
left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.subheader("Overview")

    kpi_cols = st.columns(3)
    if "value" in county_view.columns and county_view["value"].notna().any():
        vals = county_view["value"].dropna()
        kpi_cols[0].metric("Average", f"{vals.mean():.2f}")
        kpi_cols[1].metric("Median", f"{vals.median():.2f}")
        kpi_cols[2].metric("Count", f"{len(vals):,}")
    else:
        st.info("No numeric values available for this selection.")

    with st.expander("What this means"):
        st.write(
            f"""
            You’re viewing **{measure}** for **{state}**.
            Use this to compare counties, spot patterns, and identify potential areas for targeted health intervention.
            """
        )
        st.write("In real use, pair this with local context and uncertainty notes.")

with right:
    st.subheader("Data preview")
    st.dataframe(county_view.head(25), use_container_width=True)

st.divider()

# ---- Auto-report export
st.subheader("📝 Auto-report (Top/Bottom 10 Counties)")

if "county" in filtered.columns and "value" in filtered.columns and filtered["value"].notna().any():
    note_text = st.text_area(
        "Add a short interpretation (optional)",
        placeholder="Example: Top counties cluster in __. Next I’d compare access to care or poverty rate…",
        height=120,
    )

    top10, bottom10 = make_rank_tables(filtered, group_col="county", value_col="value", n=10)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("### Top 10")
        st.dataframe(top10, use_container_width=True)
    with c2:
        st.markdown("### Bottom 10")
        st.dataframe(bottom10, use_container_width=True)

    md = build_markdown_report(
        state=state,
        measure=measure,
        year=year,
        top_df=top10,
        bottom_df=bottom10,
        notes=note_text,
    )

    filename = f"PLACES_{safe_filename(state)}_{safe_filename(measure)}"
    if year is not None:
        filename += f"_{year}"
    filename += ".md"

    os.makedirs("reports", exist_ok=True)
    save_path = os.path.join("reports", filename)

    colA, colB = st.columns([0.35, 0.65])
    with colA:
        if st.button("Generate & Save Report"):
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(md)
            st.success(f"Saved: {save_path}")

    with colB:
        st.download_button(
            label="Download report as Markdown",
            data=md.encode("utf-8"),
            file_name=filename,
            mime="text/markdown",
        )

    with st.expander("Preview Markdown"):
        st.markdown(md)

else:
    st.info("Not enough fields to generate a county ranking report for this selection.")

st.divider()

# ---- Charts
st.subheader("Visuals")

if "county" in filtered.columns and "value" in filtered.columns and filtered["value"].notna().any():
    fig = bar_top_bottom(filtered, group_col="county", value_col="value", n=10)
    st.pyplot(fig, clear_figure=True)
else:
    st.warning("Not enough fields to chart top/bottom counties for this selection.")

if (
    "year" in county_view.columns
    and "value" in county_view.columns
    and county not in (None, "All")
    and county_view["year"].notna().any()
):
    st.subheader(f"Trend for {county}")
    fig2 = line_over_time(county_view, x_col="year", y_col="value")
    st.pyplot(fig2, clear_figure=True)

st.caption("Built with Streamlit • Designed for clear data storytelling.")
