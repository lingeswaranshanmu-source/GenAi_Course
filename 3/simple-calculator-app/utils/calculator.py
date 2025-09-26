# utils/calculator.py

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float):
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

def calculate(a: float, b: float, operation: str):
    if operation == "Add (+)":
        return add(a, b)
    elif operation == "Subtract (–)":
        return subtract(a, b)
    elif operation == "Multiply (×)":
        return multiply(a, b)
    elif operation == "Divide (÷)":
        return divide(a, b)
    else:
        return "Invalid operation"
