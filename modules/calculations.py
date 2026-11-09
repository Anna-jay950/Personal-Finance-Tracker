from decimal import Decimal
from modules.transactions import transactions

def calculate_balance():
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction["type"] == "income":
            total_income += transaction["amount"]
        else:
            total_expense += transaction["amount"]

    balance = total_income - total_expense

    print("\n===Financial Statement===\n")
    print(f"Total Income: GH₵{Decimal(total_income) / 100:.2f}")
    print(f"Total Expenses: GH₵{Decimal(total_expense) / 100:.2f}")
    print(f"Available Balance: GH₵{Decimal(balance) / 100:.2f}")

