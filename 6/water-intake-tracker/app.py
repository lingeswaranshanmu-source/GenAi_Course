# app.py
import streamlit as st
import matplotlib.pyplot as plt
from utils.hydration import add_entry, get_daily_total, get_weekly_data
from datetime import datetime

st.set_page_config(page_title="Water Intake Tracker 💧", page_icon="💧", layout="centered")

# --- Init Session State ---
if "entries" not in st.session_state:
    st.session_state.entries = []
if "goal" not in st.session_state:
    st.session_state.goal = 3000  # default: 3L in ml
if "unit" not in st.session_state:
    st.session_state.unit = "ml"

# --- Sidebar Navigation ---
menu = st.sidebar.radio("Navigation", ["Log Intake", "Weekly Chart", "Settings"])

# --- Log Intake Screen ---
if menu == "Log Intake":
    st.title("💧 Log Your Water Intake")

    amount = st.number_input("Amount (ml)", min_value=50, step=50)
    if st.button("Log Intake"):
        st.session_state.entries = add_entry(st.session_state.entries, amount)
        st.success(f"Logged {amount} ml!")

    # Progress
    daily_total = get_daily_total(st.session_state.entries)
    progress = daily_total / st.session_state.goal
    st.subheader("Daily Progress")
    st.progress(min(progress, 1.0))
    st.write(f"Total: {daily_total/1000:.2f} L / {st.session_state.goal/1000:.2f} L")

    remaining = st.session_state.goal - daily_total
    if remaining > 0:
        st.info(f"You need {remaining/1000:.2f} L more to reach your goal.")
    else:
        st.success("🎉 You’ve reached your daily goal!")

# --- Weekly Chart Screen ---
elif menu == "Weekly Chart":
    st.title("📊 Weekly Hydration")
    df = get_weekly_data(st.session_state.entries)
    goal = st.session_state.goal

    fig, ax = plt.subplots()
    ax.bar(df["date"], df["total"], color="#13a4ec", label="Actual")
    ax.axhline(goal, color="red", linestyle="--", label="Goal")
    ax.set_ylabel("ml")
    ax.set_title("7-Day Water Intake")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- Settings Screen ---
elif menu == "Settings":
    st.title("⚙️ App Settings")

    # Daily Goal
    new_goal = st.number_input("Daily Goal (L)", min_value=1.0, value=st.session_state.goal/1000.0, step=0.5)
    if st.button("Save Goal"):
        st.session_state.goal = int(new_goal * 1000)
        st.success(f"Daily goal updated to {new_goal} L")

    # Units
    unit = st.selectbox("Units", ["ml", "L", "oz"], index=["ml", "L", "oz"].index(st.session_state.unit))
    st.session_state.unit = unit
    st.info(f"Current unit: {unit}")

