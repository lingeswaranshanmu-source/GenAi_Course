# app.py
import streamlit as st
from utils.bmi import calculate_bmi, bmi_category

st.set_page_config(page_title="BMI Calculator", page_icon="🏋️", layout="centered")

st.title("🏋️ BMI Calculator")
st.write("Calculate your Body Mass Index (BMI) and check your health category.")

# --- Inputs ---
st.header("Enter your details")

col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
with col2:
    height = st.number_input("Height (cm)", min_value=1.0, step=0.1)

# --- Calculate ---
if st.button("Calculate BMI"):
    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)

    st.subheader("Results")
    if bmi > 0:
        st.success(f"Your BMI is **{bmi}**")
        st.info(f"Category: **{category}**")
    else:
        st.error("Please enter valid height and weight values.")
