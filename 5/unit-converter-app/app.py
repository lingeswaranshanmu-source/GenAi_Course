# app.py
import streamlit as st
from utils.converters import convert_temperature, convert_length, convert_weight
from utils.currency import convert_currency

st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")

st.title("🔄 Unit Converter App")
st.write("Convert currency, temperature, length, and weight instantly.")

# --- Category Selection ---
category = st.selectbox("Select conversion type", ["Currency", "Temperature", "Length", "Weight"])

value = st.number_input("Enter value", value=1.0, step=0.1)

# --- Conversion Logic ---
if category == "Currency":
    st.subheader("Currency Conversion")
    from_currency = st.selectbox("From", ["USD", "EUR", "INR", "GBP", "JPY"])
    to_currency = st.selectbox("To", ["USD", "EUR", "INR", "GBP", "JPY"])
    if from_currency and to_currency:
        result = convert_currency(value, from_currency, to_currency)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"{value} {from_currency} = {round(result, 2)} {to_currency}")

elif category == "Temperature":
    st.subheader("Temperature Conversion")
    from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
    result = convert_temperature(value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {round(result, 2)} {to_unit}")

elif category == "Length":
    st.subheader("Length Conversion")
    from_unit = st.selectbox("From", ["meters", "kilometers", "centimeters", "inches", "feet", "miles"])
    to_unit = st.selectbox("To", ["meters", "kilometers", "centimeters", "inches", "feet", "miles"])
    result = convert_length(value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {round(result, 4)} {to_unit}")

elif category == "Weight":
    st.subheader("Weight Conversion")
    from_unit = st.selectbox("From", ["grams", "kilograms", "pounds", "ounces", "tons"])
    to_unit = st.selectbox("To", ["grams", "kilograms", "pounds", "ounces", "tons"])
    result = convert_weight(value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {round(result, 4)} {to_unit}")
