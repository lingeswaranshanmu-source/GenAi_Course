# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🎉 Event Registration System", page_icon="🎉", layout="centered")

# --- Initialize session state ---
if "registrations" not in st.session_state:
    st.session_state.registrations = []

# --- Registration Form ---
st.title("🎉 Event Registration")

with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    event_choice = st.selectbox("Select Event", ["Workshop A", "Workshop B", "Workshop C"])
    submitted = st.form_submit_button("Register")

    if submitted:
        if name.strip() and email.strip() and event_choice:
            st.session_state.registrations.append({
                "Name": name.strip(),
                "Email": email.strip(),
                "Event": event_choice,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success(f"✅ Thanks {name}, you are registered for **{event_choice}**!")
        else:
            st.error("⚠️ Please fill all fields")

# --- Live Count ---
st.subheader("📊 Total Registrations")
st.metric(label="Registered Participants", value=len(st.session_state.registrations))

# --- Organizer View ---
if st.session_state.registrations:
    st.markdown("### 👥 Registered Participants")
    df = pd.DataFrame(st.session_state.registrations)
    st.dataframe(df, use_container_width=True)

    # --- CSV Export ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"registrations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )
