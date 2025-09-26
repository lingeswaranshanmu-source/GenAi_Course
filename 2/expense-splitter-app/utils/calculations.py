# utils/calculations.py
import pandas as pd

def calculate_equal_split(total_amount: float, num_people: int) -> float:
    """Return equal share for each person."""
    return round(total_amount / num_people, 2)

def calculate_balances(total_amount: float, people: list[dict]) -> pd.DataFrame:
    """Return a dataframe with name, contribution, expected, and balance."""
    num_people = len(people)
    equal_share = calculate_equal_split(total_amount, num_people)

    results = []
    for p in people:
        contribution = float(p["contribution"])
        balance = round(contribution - equal_share, 2)
        results.append({
            "Name": p["name"],
            "Contribution": contribution,
            "Expected": equal_share,
            "Balance": balance,
            "Status": (
                f"Owes {abs(balance)}" if balance < 0
                else f"Gets back {balance}" if balance > 0
                else "Settled"
            )
        })
    return pd.DataFrame(results)
