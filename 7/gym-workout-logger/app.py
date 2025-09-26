# app.py
import streamlit as st
import matplotlib.pyplot as plt
from utils.workouts import load_data, log_exercise, get_history_df, calculate_weekly_progress

st.set_page_config(page_title="Gym Workout Logger 🏋️", page_icon="🏋️", layout="wide")

# --- Load Data ---
if "exercises" not in st.session_state:
    st.session_state.exercises = load_data()

# --- Store last action message ---
if "last_message" not in st.session_state:
    st.session_state.last_message = None

# --- Sidebar Navigation ---
menu = st.sidebar.radio("Navigation", ["Log Workout", "History", "Weekly Progress"])

# --- Log Workout Screen ---
if menu == "Log Workout":
    st.title("🏋️ Log a Workout")

    # Input fields with session state keys
    name = st.text_input("Exercise Name", key="exercise_name")
    sets = st.number_input("Sets", min_value=1, step=1, key="exercise_sets")
    reps = st.number_input("Reps", min_value=1, step=1, key="exercise_reps")
    weight = st.number_input("Weight (kg)", min_value=1.0, step=1.0, key="exercise_weight")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add Entry"):
            st.session_state.exercises = log_exercise(
                st.session_state.exercises, name, sets, reps, weight
            )
            st.session_state.last_message = f"✅ Logged: {sets}×{reps} {name} at {weight} kg"
            st.rerun()

    with col2:
        if st.button("Reset Form"):
            st.session_state.update({
                "exercise_name": "",
                "exercise_sets": 1,
                "exercise_reps": 1,
                "exercise_weight": 1.0,
                "last_message": "Form reset."
            })
            st.rerun()

    # Show last action message (after rerun)
    if st.session_state.last_message:
        st.success(st.session_state.last_message)

# --- History Screen ---
elif menu == "History":
    st.title("📜 Workout History")
    df = get_history_df(st.session_state.exercises)
    if df.empty:
        st.info("No workouts logged yet.")
    else:
        st.dataframe(df, use_container_width=True)

# --- Weekly Progress Screen ---
elif menu == "Weekly Progress":
    st.title("📊 Weekly Progress")
    weekly = calculate_weekly_progress(st.session_state.exercises)
    if weekly.empty:
        st.info("No data to display. Log workouts first.")
    else:
        fig, ax = plt.subplots()
        ax.bar(weekly["week"], weekly["total_volume"], color="#4CAF50")
        ax.set_ylabel("Total Volume (kg)")
        ax.set_xlabel("Week")
        ax.set_title("Weekly Training Volume")
        plt.xticks(rotation=45)
        st.pyplot(fig)
