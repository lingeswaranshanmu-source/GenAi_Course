# app.py
import streamlit as st
from utils.calculator import calculate

st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

# --- Initialize session state defaults ---
defaults = {
    "num1": 0.0,
    "num2": 0.0,
    "operation": "Add (+)",
    "result": None,
    "error": None,
    "history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.title("🧮 Simple Calculator App")
st.write("Perform basic arithmetic operations quickly and easily.")

# --- Input widgets (bound to session_state keys) ---
st.header("Enter Numbers")
col1, col2 = st.columns(2)
with col1:
    st.number_input("First Number", key="num1", format="%.6g")
with col2:
    st.number_input("Second Number", key="num2", format="%.6g")

# --- Operation selection ---
st.header("Select Operation")
st.radio(
    "Choose an operation",
    ["Add (+)", "Subtract (–)", "Multiply (×)", "Divide (÷)"],
    key="operation",
    horizontal=True,
)

# --- Calculate and Reset buttons ---
calc_col, reset_col = st.columns([3, 1])

with calc_col:
    if st.button("Calculate"):
        # reset previous result/error
        st.session_state["result"] = None
        st.session_state["error"] = None

        # Read inputs from session_state (widgets keep them updated)
        try:
            a = float(st.session_state["num1"])
            b = float(st.session_state["num2"])
        except Exception:
            st.session_state["error"] = "Invalid input. Please enter valid numbers."
            st.session_state["result"] = None
        else:
            res = calculate(a, b, st.session_state["operation"])
            if isinstance(res, str):
                # calculate returned an error message (e.g., divide by zero)
                st.session_state["error"] = res
                st.session_state["result"] = None
            else:
                st.session_state["result"] = res
                st.session_state["error"] = None
                # add to history (most recent first), keep max 10
                hist = st.session_state.get("history", [])
                hist.insert(0, {"a": a, "b": b, "op": st.session_state["operation"], "res": res})
                st.session_state["history"] = hist[:10]

with reset_col:
    if st.button("Reset"):
        # Reset only the relevant keys to sensible defaults
        st.session_state["num1"] = 0.0
        st.session_state["num2"] = 0.0
        st.session_state["operation"] = "Add (+)"
        st.session_state["result"] = None
        st.session_state["error"] = None
        st.session_state["history"] = []
        # rerun to immediately reflect cleared values in the UI
        st.rerun()

# --- Result display ---
st.markdown("---")
st.subheader("Result")

if st.session_state["error"]:
    st.error(st.session_state["error"])
elif st.session_state["result"] is not None:
    # Format result neatly (avoid long float strings)
    formatted = "{:.10g}".format(st.session_state["result"])
    st.success(f"The result of **{st.session_state['operation']}** is: **{formatted}**")
else:
    st.info("Enter numbers and choose an operation, then press **Calculate**.")

# --- Optional: show small history of last calculations ---
if st.session_state.get("history"):
    st.markdown("### Recent calculations")
    for item in st.session_state["history"]:
        a, b, op, r = item["a"], item["b"], item["op"], item["res"]
        formatted = "{:.10g}".format(r)
        st.write(f"- `{a}` {op} `{b}` = **{formatted}**")

# Debugging expander (remove for production)
with st.expander("Session state (debug)"):
    st.json({k: st.session_state.get(k) for k in st.session_state.keys()})
