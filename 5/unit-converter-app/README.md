# 🔄 Unit Converter App

A Streamlit app to convert **currency, temperature, length, and weight** instantly.

## Features
- Currency (USD, EUR, INR, GBP, JPY) with live rates
- Temperature (C, F, K)
- Length (m, km, cm, in, ft, miles)
- Weight (g, kg, lbs, oz, tons)

## Run locally
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
