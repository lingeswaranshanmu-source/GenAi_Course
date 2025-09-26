# utils/converters.py

# --- Temperature ---
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
    return value

# --- Length ---
LENGTH_FACTORS = {
    "meters": 1,
    "kilometers": 1000,
    "centimeters": 0.01,
    "inches": 0.0254,
    "feet": 0.3048,
    "miles": 1609.34,
}

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    meters = value * LENGTH_FACTORS[from_unit]
    return meters / LENGTH_FACTORS[to_unit]

# --- Weight ---
WEIGHT_FACTORS = {
    "grams": 1,
    "kilograms": 1000,
    "pounds": 453.592,
    "ounces": 28.3495,
    "tons": 1_000_000,
}

def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    grams = value * WEIGHT_FACTORS[from_unit]
    return grams / WEIGHT_FACTORS[to_unit]
