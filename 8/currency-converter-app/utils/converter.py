# utils/converter.py

# Static conversion rates (base = USD)
RATES = {
    "USD": 1,
    "INR": 83.25,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 148.5,
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert amount between currencies using static rate table."""
    if from_currency not in RATES or to_currency not in RATES:
        raise ValueError("Unsupported currency")

    if from_currency == to_currency:
        return round(amount, 2)

    rate_from = RATES[from_currency]
    rate_to = RATES[to_currency]

    converted = amount * (rate_to / rate_from)
    return round(converted, 2)
