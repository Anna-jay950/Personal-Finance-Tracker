import shutil
import json
from pathlib import Path
from datetime import datetime, date
from modules.data_manager import DATA_FILE, save_transactions

DATA_BACKUP_DIR = Path(__file__).resolve().parent.parent / "backups"

def create_backup(backup_type = "manual"):

    DATA_BACKUP_DIR.mkdir(parents=True, exist_ok=True)

   # Check whether the main data file exists
    if not DATA_FILE.exists():
        raise FileNotFoundError("No transaction file available to back up.")

    # Generate a unique timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Create the backup filename
    backup_name = f"backup_{backup_type}_{timestamp}.json"

    backup_path = DATA_BACKUP_DIR / backup_name

    # Copy the main data file
    shutil.copy2(DATA_FILE, backup_path)

    return backup_path

def manual_backup():

    try:
        backup_path = create_backup("manual")

        print("\nManual backup created successfully!")
        print(f"Backup file: {backup_path.name}")

    except OSError as error:
        print(f"\nUnable to create backup: {error}")


def view_backups():

    backups = sorted(
        DATA_BACKUP_DIR.glob("backup_*.json"),
        reverse=True
    )

    if not backups:
        print("\nNo backups available.")
        return []

    print("\n========== BACKUP HISTORY ==========")

    for index, backup in enumerate(backups, start=1):
        print(f"{index}. {backup.name}")

    return backups

def validate_backup(backup_path):

    try:
        with open(backup_path, "r", encoding="utf-8") as file:
            backup_data = json.load(file)

    except json.JSONDecodeError:
        raise ValueError("This backup contains invalid JSON.")

    # Check that the backup contains a list
    if not isinstance(backup_data, list):
        raise ValueError("Backup must contain a list of transactions.")

    # Check every transaction
    required_fields = [
        "id", "type", "description",
        "amount", "category", "date"
    ]

    for transaction in backup_data:

        if not isinstance(transaction, dict):
            raise ValueError("A transaction record is not valid.")

        # Check required fields
        for field in required_fields:
            if field not in transaction:
                raise ValueError(f"Missing transaction field: {field}")

        # Check transaction type
        if transaction["type"] not in ["income", "expense"]:
            raise ValueError("Invalid transaction type.")

        # Check amount
        if type(transaction["amount"]) is not int or transaction["amount"] <= 0:
            raise ValueError("Invalid transaction amount.")

        # Check text fields
        for field in ["id", "description", "category"]:
            if not isinstance(transaction[field], str) or not transaction[field].strip():
                raise ValueError(f"Invalid {field}.")

        # Check date
        try:
            date.fromisoformat(transaction["date"])
        except (ValueError, TypeError):
            raise ValueError("Invalid transaction date.")

    return backup_data

def restore_backup(backup_path):

    # Step 1: Validate the selected backup
    restored_transactions = validate_backup(backup_path)

    # Step 2: Create a safety backup of current data
    if DATA_FILE.exists():
        create_backup("safety")

    # Step 3: Replace the current transaction data
    save_transactions(restored_transactions)

    print("\nBackup restored successfully!")

    return restored_transactions