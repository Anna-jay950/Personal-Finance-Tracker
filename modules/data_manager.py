import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent /"data" / "transactions.json"

def save_transactions(transactions):

     # Ensure the data folder exists
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file first
    temporary_file = DATA_FILE.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4)

    # Replace the old file with the updated file
    temporary_file.replace(DATA_FILE)


def load_transactions():

    # If the file does not exist, create it
    if not DATA_FILE.exists():
        save_transactions([])
        return []

    # Read existing transaction records
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            transactions = json.load(file)

    except json.JSONDecodeError:
        raise ValueError("The transaction file contains invalid JSON.")

    # Ensure the stored data is a list
    if not isinstance(transactions, list):
        raise ValueError("The transaction file must contain a list.")

    return transactions