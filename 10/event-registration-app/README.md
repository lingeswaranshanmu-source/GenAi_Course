# 🎉 Event Registration System

A simple Streamlit app to collect event registrations, track live counts, and export data as CSV.

## Features
- Registration form: Name, Email, Event Choice
- Stores data in `st.session_state` (in memory)
- Live registration count
- Organizer view with table
- CSV export

## Run locally
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
