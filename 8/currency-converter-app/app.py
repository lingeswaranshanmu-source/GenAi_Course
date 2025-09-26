# app.py
import streamlit as st
from utils.converter import convert_currency, RATES

st.set_page_config(page_title="Currency Converter 💱", page_icon="💱", layout="centered")

st.title("💱 Currency Converter")
st.write("Convert between currencies using static exchange rates (offline mode).")

# --- Inputs ---
amount = st.number_input("Enter amount", min_value=0.0, step=1.0, value=100.0)

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("From Currency", list(RATES.keys()), index=1)  # default INR
with col2:
    to_currency = st.selectbox("To Currency", list(RATES.keys()), index=0)  # default USD

# --- Conversion ---
if amount > 0:
    result = convert_currency(amount, from_currency, to_currency)
    st.subheader("Result")
    st.success(f"{amount} {from_currency} = {result} {to_currency}")
else:
    st.error("Please enter a valid amount greater than 0.")
