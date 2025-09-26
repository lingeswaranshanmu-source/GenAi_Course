# app.py
import streamlit as st
import pandas as pd
from utils.calculations import calculate_equal_split, calculate_balances

st.set_page_config(page_title="Expense Splitter App", page_icon="💰", layout="centered")

st.title("💰 Expense Splitter App")
st.write("Easily split expenses among friends and see who owes or gets back money.")

# --- Inputs ---
st.header("Step 1: Enter Expense Details")
total_amount = st.number_input("Total Amount", min_value=0.0, format="%.2f")
num_people = st.number_input("Number of People", min_value=1, step=1)

# Equal split quick calculation
if total_amount > 0 and num_people > 0:
    equal_share = calculate_equal_split(total_amount, num_people)
    st.info(f"Equal split: Each person should pay **{equal_share}**")

# --- Contributions ---
st.header("Step 2: Enter Individual Contributions (optional)")

people_data = []
if num_people > 0:
    for i in range(int(num_people)):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
        with col2:
            contribution = st.number_input(f"Contribution {i+1}", min_value=0.0, format="%.2f", key=f"contribution_{i}")
        if name.strip():
            people_data.append({"name": name.strip(), "contribution": contribution})

# --- Results ---
if st.button("Calculate Split"):
    if not people_data:
        st.warning("Please enter at least one name + contribution.")
    else:
        df = calculate_balances(total_amount, people_data)
        st.subheader("Results")
        st.dataframe(df, use_container_width=True)

        st.write("### Summary:")
        for _, row in df.iterrows():
            st.write(f"- {row['Name']}: {row['Status']} (Contributed {row['Contribution']}, Expected {row['Expected']})")

        # Double-check total balances out to 0
        st.write(f"**Check:** Sum of balances = {df['Balance'].sum()}")
