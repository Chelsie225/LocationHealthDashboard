# PLACES Public Health Dashboard (Streamlit)

A small, recruiter-friendly data app that downloads CDC PLACES county-level data and lets you filter by state/measure (and year if available), view summary stats, and generate a **Top/Bottom 10 counties** Markdown report.

## What this demonstrates
- Clean project structure (app/ + src/)
- Working UI with filters, KPIs, charts, and data preview
- Data fetching + caching
- Exportable artifacts (Markdown report) for quick sharing

## Run locally

### 1) Create a virtual environment (recommended)
**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Start the app
```bash
streamlit run app/streamlit_app.py
```

The first run may take a little longer while it downloads the dataset.

## Notes
- Data source: CDC PLACES (downloaded from data.cdc.gov).
- This project is for learning/demo purposes; do not use alone for real policy decisions.
