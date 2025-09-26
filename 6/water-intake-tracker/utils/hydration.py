# utils/hydration.py
import pandas as pd
from datetime import datetime, timedelta

def add_entry(entries, amount):
    """Log new water intake entry."""
    today = datetime.now().strftime("%Y-%m-%d")
    entries.append({"date": today, "amount": amount})
    return entries

def get_daily_total(entries, date=None):
    """Aggregate daily intake for a given date."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return sum(e["amount"] for e in entries if e["date"] == date)

def get_weekly_data(entries):
    """Return last 7 days totals as DataFrame."""
    today = datetime.now()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    data = []
    for d in days:
        total = sum(e["amount"] for e in entries if e["date"] == d)
        data.append({"date": d, "total": total})
    return pd.DataFrame(data)
