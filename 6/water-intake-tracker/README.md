# 💧 Water Intake Tracker

A Streamlit app to log daily water intake, track progress toward goals, and view weekly hydration charts.

## Features
- Log multiple water intakes per day
- Daily progress bar (default goal: 3L/day)
- Weekly hydration chart
- Settings to update daily goal and units

## Run locally
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
