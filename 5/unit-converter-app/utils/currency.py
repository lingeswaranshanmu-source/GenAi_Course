# utils/currency.py
import requests

API_URL = "https://open.er-api.com/v6/latest/{}"  # free exchange rate API

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float | str:
    try:
        resp = requests.get(API_URL.format(from_currency))
        if resp.status_code != 200:
            return "Error: Failed to fetch exchange rates"
        data = resp.json()
        rates = data.get("rates", {})
        if to_currency not in rates:
            return f"Error: {to_currency} not available"
        return amount * rates[to_currency]
    except Exception as e:
        return f"Error: {e}"
