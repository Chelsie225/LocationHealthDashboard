# PLACES Public Health Dashboard

An interactive data dashboard built with **Streamlit** for exploring CDC PLACES county-level public health estimates. The application allows users to filter by state, health measure,
and year (when available), visualize trends and comparisons, and generate automated **Top/Bottom 10 county reports** in Markdown format.

---

## Project Overview

This project demonstrates how public health data can be transformed into an accessible, interactive tool for exploration and quick insight generation. It is designed to prioritize clarity, 
usability, and responsible data handling rather than complex modeling.

Key features include:
- Interactive filtering by state, county, health measure, and year
- Summary statistics (average, median, count) for selected views
- Visual comparisons of top and bottom counties
- Optional time-series trends for individual counties
- Automated, exportable Markdown reports for sharing insights

---

## Tech Stack

- **Python**
- **Streamlit** – the interactive UI
- **Pandas / NumPy** – handling data
- **Matplotlib** – visualizations
- **Requests** – data retrieval

---

## Data Source

- **CDC PLACES (Population Level Analysis and Community Estimates)**  
  County-level model-based estimates of health outcomes, behaviors, and preventive measures.

> Note: PLACES data are statistical estimates and should be interpreted with appropriate context and caution.


---

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/places-health-dashboard.git
cd places-health-dashboard

### 2. Create and activate a virtual enviornment
For Windows:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
For Mac/Linux:
python3 -m venv .venv
source .venv/bin/activate
### 3.Install Dependencies
python -m pip install -r requirements.txt
### 4. Run the Streamlitapp
python -m streamlit run app/streamlit_app.py

The dashboard will open in your browser at **http://localhost:8501.**



