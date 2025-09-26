# 🏋️ Gym Workout Logger

A Streamlit app to log gym workouts, view history, and track weekly progress.

## Features
- Log exercises (sets, reps, weight)
- Persistent storage (local JSON file)
- Workout history table
- Weekly progress chart (total volume)

## Run locally
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
