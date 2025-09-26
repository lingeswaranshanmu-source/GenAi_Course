# utils/bmi.py

def calculate_bmi(weight: float, height: float) -> float:
    """Calculate BMI given weight (kg) and height (cm)."""
    if height <= 0:
        return 0
    height_m = height / 100  # convert cm to meters
    return round(weight / (height_m ** 2), 2)


def bmi_category(bmi: float) -> str:
    """Return health category based on BMI value."""
    if bmi <= 0:
        return "Invalid input"
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"
