# app.py
import streamlit as st
import html
from typing import Optional

st.set_page_config(page_title="FormApp", page_icon="📝", layout="centered")

# --- Helpers ---
def sanitize_name(name: str) -> str:
    # Basic sanitization: strip whitespace, escape HTML
    return html.escape(name.strip())

def validate_name(name: str) -> Optional[str]:
    t = name.strip()
    if len(t) < 2:
        return "Please enter at least 2 characters."
    if not all(c.isalpha() or c.isspace() or c in "-.'" for c in t):
        return "Name may contain letters, spaces, and - ' . characters only."
    return None

# --- Initialize session state ---
if "saved_name" not in st.session_state:
    st.session_state["saved_name"] = ""
if "saved_age" not in st.session_state:
    st.session_state["saved_age"] = None
if "current_name" not in st.session_state:
    st.session_state["current_name"] = ""
if "current_age" not in st.session_state:
    st.session_state["current_age"] = 25
if "name_error" not in st.session_state:
    st.session_state["name_error"] = ""

# --- Layout ---
st.markdown("<h1 style='text-align:center'>Let's Get Started</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#6b7280'>Fill in the details below.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Name")
    name_input = st.text_input("Enter your full name", value=st.session_state["current_name"], key="name_input")
    if st.button("Continue", key="save_name"):
        st.session_state["current_name"] = name_input
        error = validate_name(name_input)
        if error:
            st.session_state["name_error"] = error
        else:
            st.session_state["name_error"] = ""
            st.session_state["saved_name"] = sanitize_name(name_input)

    if st.session_state["name_error"]:
        st.error(st.session_state["name_error"])

with col2:
    st.subheader("Your Age")
    age = st.slider("Select your age", 1, 100, value=st.session_state["current_age"], key="age_slider")
    if st.button("Continue", key="save_age"):
        st.session_state["current_age"] = age
        st.session_state["saved_age"] = int(age)

# Greeting box (only when both saved)
if st.session_state["saved_name"] and st.session_state["saved_age"] is not None:
    st.markdown(
        f"""
        <div style="
            margin-top: 32px;
            padding: 18px;
            border-radius: 10px;
            background: #ffffff;
            box-shadow: 0 6px 18px rgba(10,10,10,0.06);
            text-align:center;
            font-size:18px;
        ">
            Hello, <strong style="color:#0b6ef6">{st.session_state['saved_name']}</strong>! You are <strong style="color:#0b6ef6">{st.session_state['saved_age']}</strong> years old.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Please enter your name and age, then click Continue on each card to see your personalized greeting.")
