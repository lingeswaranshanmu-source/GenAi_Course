# utils/workouts.py
import json
import os
from datetime import datetime
import pandas as pd

DATA_FILE = "workouts.json"

def load_data():
    """Load workout data from JSON file, safely handling empty or corrupted files."""
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        # If file is corrupted, reset to empty list
        return []

def save_data(data):
    """Save workout data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_exercise(exercises, name, sets, reps, weight):
    """Log a new exercise entry with timestamp."""
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "exercise": name,
        "sets": int(sets),
        "reps": int(reps),
        "weight": float(weight),
    }
    exercises.append(entry)
    save_data(exercises)
    return exercises

def get_history_df(exercises):
    """Return workout history as a DataFrame."""
    if not exercises:
        return pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight"])
    return pd.DataFrame(exercises)

def calculate_weekly_progress(exercises):
    """Aggregate total training volume per week."""
    df = get_history_df(exercises)
    if df.empty:
        return pd.DataFrame(columns=["week", "total_volume"])
    
    df["volume"] = df["sets"] * df["reps"] * df["weight"]
    df["week"] = pd.to_datetime(df["date"]).dt.strftime("%Y-W%U")
    weekly = df.groupby("week")["volume"].sum().reset_index(name="total_volume")
    return weekly
