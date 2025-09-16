import streamlit as st

# Page title
st.title("🚀 Hello, Streamlit app!")

# Input field
name = st.text_input("Enter your name", "World")

# Button
if st.button("👋 Say Hello"):
    if name.strip():
        st.success(f"Hello, {name}! 🎉 Well done!")
    else:
        st.error("⚠️ Please enter your name.")

