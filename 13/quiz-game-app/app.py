# app.py
import streamlit as st
import random
import copy
import pandas as pd
from io import StringIO
from datetime import datetime

st.set_page_config(page_title="Quiz Game App ❓", page_icon="❓", layout="centered")

# ---------------------------
# Hardcoded questions
# ---------------------------
# Note: keep 'answer' text exactly matching one of 'options'
QUESTIONS = [
    {"id": 1, "question": "What is the capital of France?",
     "options": ["Paris", "Berlin", "Rome", "Madrid"], "answer": "Paris"},
    {"id": 2, "question": "2 + 2 = ?",
     "options": ["3", "4", "5"], "answer": "4"},
    {"id": 3, "question": "Largest planet in the Solar System?",
     "options": ["Earth", "Jupiter", "Mars"], "answer": "Jupiter"},
    {"id": 4, "question": "Who wrote 'Hamlet'?",
     "options": ["Charles Dickens", "William Shakespeare", "Leo Tolstoy"], "answer": "William Shakespeare"},
    {"id": 5, "question": "Which language is primarily used for iOS development?",
     "options": ["Swift", "Kotlin", "Ruby", "Go"], "answer": "Swift"},
]

# ---------------------------
# Utility functions
# ---------------------------
def build_quiz(shuffle_questions=True, shuffle_options=True):
    """Return a deep copy of QUESTIONS, optionally shuffled (questions and their options)."""
    quiz = copy.deepcopy(QUESTIONS)
    if shuffle_questions:
        random.shuffle(quiz)
    if shuffle_options:
        for q in quiz:
            random.shuffle(q["options"])
    return quiz

def init_state(shuffle_questions=True, shuffle_options=True):
    """Initialize session state for a new quiz run."""
    if "quiz" not in st.session_state:
        st.session_state.quiz = build_quiz(shuffle_questions, shuffle_options)
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []  # list of dicts with selected/correct/etc.
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "shuffle_questions" not in st.session_state:
        st.session_state.shuffle_questions = shuffle_questions
    if "shuffle_options" not in st.session_state:
        st.session_state.shuffle_options = shuffle_options

def reset_quiz(shuffle_questions=True, shuffle_options=True):
    """Reset quiz state and optionally reshuffle."""
    st.session_state.quiz = build_quiz(shuffle_questions, shuffle_options)
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.finished = False
    st.session_state.shuffle_questions = shuffle_questions
    st.session_state.shuffle_options = shuffle_options
    # rerun to update UI cleanly
    st.rerun()

def submit_answer(selected_option):
    """Evaluate selected option, update score & answers, advance to next question or finish."""
    idx = st.session_state.current_q
    q = st.session_state.quiz[idx]
    is_correct = (selected_option == q["answer"])
    if is_correct:
        st.session_state.score += 1
    st.session_state.answers.append({
        "id": q["id"],
        "question": q["question"],
        "selected": selected_option,
        "correct": q["answer"],
        "is_correct": is_correct
    })
    st.session_state.current_q += 1
    if st.session_state.current_q >= len(st.session_state.quiz):
        st.session_state.finished = True
    st.rerun()

# ---------------------------
# App UI
# ---------------------------
st.title("❓ Quiz Game App")
st.write("Answer the questions; your score will be tracked for this session.")

# Sidebar: quiz options
with st.sidebar:
    st.header("Quiz Settings")
    shuffle_q = st.checkbox("Shuffle questions", value=True)
    shuffle_o = st.checkbox("Shuffle options", value=True)
    if st.button("Restart with settings"):
        # Reset with chosen settings
        reset_quiz(shuffle_questions=shuffle_q, shuffle_options=shuffle_o)

# Initialize state (only if keys missing)
init_state(shuffle_questions=True, shuffle_options=True)

# Main flow
if st.session_state.finished:
    st.subheader("🎉 Quiz Finished!")
    st.write(f"Your score: **{st.session_state.score} / {len(st.session_state.quiz)}**")

    st.markdown("### Review your answers")
    df = pd.DataFrame(st.session_state.answers)
    if not df.empty:
        df_display = df[["question", "selected", "correct", "is_correct"]].rename(
            columns={"question": "Question", "selected": "Your Answer", "correct": "Correct Answer", "is_correct": "Correct?"}
        )
        # show color-coded table: we can't color cells directly easily; show table and separate legend
        st.table(df_display)

        # CSV export of results
        csv_buffer = StringIO()
        csv_df = df[["question", "selected", "correct", "is_correct"]].rename(
            columns={"question": "Question", "selected": "Your Answer", "correct": "Correct Answer", "is_correct": "Correct?"}
        )
        csv_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")
        st.download_button(
            "⬇️ Download results (CSV)",
            data=csv_bytes,
            file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No answers recorded (unexpected).")

    if st.button("🔁 Restart Quiz"):
        reset_quiz(shuffle_questions=st.session_state.shuffle_questions, shuffle_options=st.session_state.shuffle_options)

else:
    q_idx = st.session_state.current_q
    q = st.session_state.quiz[q_idx]
    st.write(f"**Question {q_idx + 1} of {len(st.session_state.quiz)}**")
    st.write(q["question"])
    # radio with a unique key so Streamlit stores the selection per question index
    choice_key = f"choice_{q_idx}"
    selected = st.radio("Choose an answer:", q["options"], key=choice_key)

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("✅ Submit"):
            if not selected:
                st.warning("⚠️ Please select an option before submitting.")
            else:
                submit_answer(selected)
    with col2:
        if st.button("⏮️ Previous"):
            # allow going back one question (optional); do not change score or answers - simple approach
            if st.session_state.current_q > 0:
                # remove last stored answer only if it exists (we store answers only on submit)
                if st.session_state.answers:
                    # we only allow previous if last recorded corresponds to previous index
                    # pop last answer and decrement score if it was correct
                    last = st.session_state.answers.pop()
                    if last["is_correct"]:
                        st.session_state.score = max(0, st.session_state.score - 1)
                st.session_state.current_q = max(0, st.session_state.current_q - 1)
                st.rerun()
    with col3:
        if st.button("🔄 Reset Quiz"):
            reset_quiz(shuffle_questions=st.session_state.shuffle_questions, shuffle_options=st.session_state.shuffle_options)

    # show progress
    st.markdown("---")
    st.info(f"Progress: **{q_idx} / {len(st.session_state.quiz)}** completed • Score: **{st.session_state.score}**")
