# app.py
import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Rock Paper Scissors", page_icon="✊📄✂️", layout="centered")

# --- Helpers ---
CHOICES = ["Rock", "Paper", "Scissors"]

def decide_winner(user, comp):
    if user == comp:
        return "Tie"
    win_conditions = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }
    return "User" if win_conditions[user] == comp else "Computer"

def ensure_session_state():
    if "score_user" not in st.session_state:
        st.session_state.score_user = 0
    if "score_computer" not in st.session_state:
        st.session_state.score_computer = 0
    if "ties" not in st.session_state:
        st.session_state.ties = 0
    if "rounds_played" not in st.session_state:
        st.session_state.rounds_played = 0
    if "last_round" not in st.session_state:
        st.session_state.last_round = None
    if "history" not in st.session_state:
        st.session_state.history = []  # list of dicts: {time, user, computer, result}

ensure_session_state()

st.title("✊📄✂️ Rock, Paper, Scissors")
st.write("Play against the computer. Score is tracked across rounds (session only).")

# --- UI: choice buttons ---
st.subheader("Choose your move")
cols = st.columns(3)
if cols[0].button("✊ Rock", key="btn_rock"):
    user_choice = "Rock"
    comp_choice = random.choice(CHOICES)
    result = decide_winner(user_choice, comp_choice)
    st.session_state.rounds_played += 1
    if result == "Tie":
        st.session_state.ties += 1
    elif result == "User":
        st.session_state.score_user += 1
    else:
        st.session_state.score_computer += 1
    st.session_state.last_round = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   "user": user_choice, "computer": comp_choice, "result": result}
    st.session_state.history.insert(0, st.session_state.last_round)
    st.rerun()

if cols[1].button("📄 Paper", key="btn_paper"):
    user_choice = "Paper"
    comp_choice = random.choice(CHOICES)
    result = decide_winner(user_choice, comp_choice)
    st.session_state.rounds_played += 1
    if result == "Tie":
        st.session_state.ties += 1
    elif result == "User":
        st.session_state.score_user += 1
    else:
        st.session_state.score_computer += 1
    st.session_state.last_round = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   "user": user_choice, "computer": comp_choice, "result": result}
    st.session_state.history.insert(0, st.session_state.last_round)
    st.rerun()

if cols[2].button("✂️ Scissors", key="btn_scissors"):
    user_choice = "Scissors"
    comp_choice = random.choice(CHOICES)
    result = decide_winner(user_choice, comp_choice)
    st.session_state.rounds_played += 1
    if result == "Tie":
        st.session_state.ties += 1
    elif result == "User":
        st.session_state.score_user += 1
    else:
        st.session_state.score_computer += 1
    st.session_state.last_round = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   "user": user_choice, "computer": comp_choice, "result": result}
    st.session_state.history.insert(0, st.session_state.last_round)
    st.rerun()

st.markdown("---")

# --- Last round display ---
st.subheader("Last Round")
if st.session_state.last_round:
    lr = st.session_state.last_round
    st.write(f"**You:** {lr['user']}  —  **Computer:** {lr['computer']}")
    if lr["result"] == "Tie":
        st.info("Result: It's a tie!")
    elif lr["result"] == "User":
        st.success("Result: You won this round! 🎉")
    else:
        st.error("Result: Computer won this round.")

else:
    st.info("No rounds played yet — pick Rock, Paper, or Scissors above to start!")

st.markdown("---")

# --- Scoreboard ---
st.subheader("Scoreboard")
col_a, col_b, col_c = st.columns(3)
col_a.metric("You (Wins)", st.session_state.score_user)
col_b.metric("Computer (Wins)", st.session_state.score_computer)
col_c.metric("Ties", st.session_state.ties)
st.write(f"Rounds played: **{st.session_state.rounds_played}**")

# --- Controls: reset, history export ---
st.markdown("---")
controls_col1, controls_col2 = st.columns([2, 3])

with controls_col1:
    if st.button("🔁 Reset Score"):
        # reset relevant session state values safely
        st.session_state.update({
            "score_user": 0,
            "score_computer": 0,
            "ties": 0,
            "rounds_played": 0,
            "last_round": None,
            "history": []
        })
        st.success("Scoreboard reset.")
        st.rerun()

with controls_col2:
    # Download history as CSV if exists
    if st.session_state.history:
        import pandas as pd
        df = pd.DataFrame(st.session_state.history)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download History (CSV)",
            data=csv,
            file_name=f"rps_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.write("No history to export.")

st.markdown("---")

# --- Optional: show history (most recent first) ---
with st.expander("Show round history (most recent first)"):
    if not st.session_state.history:
        st.info("No rounds yet.")
    else:
        for i, h in enumerate(st.session_state.history):
            st.write(f"{i+1}. {h['time']} — You: **{h['user']}** | Computer: **{h['computer']}** — Result: **{h['result']}**")
