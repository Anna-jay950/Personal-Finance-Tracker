from modules.backups import create_backup
from modules.data_manager import save_transactions
from datetime import date
from decimal import Decimal, InvalidOperation
import uuid

income_categories = [
    "Allowance",
    "Salary",
    "Freelance",
    "Investments",
    "Gifts",
    "Other",
]

expense_categories = [
    "Food",
    "Utilities",
    "Groceries",
    "Transportation",
    "Entertainment",
    "Healthcare",
    "Education",
    "Internet",
    "Other",
]

transactions = []


def add_transaction():

    # Get transaction type

    transaction_type = (
        input("Enter transaction type (income/expense): ").strip().lower()
    )

    while transaction_type not in ["income", "expense"]:
        print("Invalid tyoe. Enter income or expense: ")
        transaction_type = input("Enter type: ").strip().lower()

    # Get description

    description = input("Enter description: ").strip()

    while not description:
        print("Description cannot be empty")
        description = input("Enter description: ").strip()

    # Get amount

    while True:
        try:
            amount = Decimal(input("Enter amount (GH₵): ").strip())

            if not amount.is_finite() or amount <= 0:
                print("Amount must be greater than zero")
                continue

            if amount != amount.quantize(Decimal("0.01")):
                print("Enter no more than two decimal places.")
                continue

            amount = int(amount * 100)
            break

        except InvalidOperation:
            print("Please enter a valid amount.")

    # Select category

    if transaction_type == "income":
        categories = income_categories
    else:
        categories = expense_categories

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    print(f"{len(categories) + 1}. Create a new category")

    while True:
        try:
            choice = int(input("Select category: "))

            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break

            elif choice == len(categories) + 1:
                category = input("Enter new category: ").strip()

                if category:
                    categories.append(category)
                    break

                print("Category cannot be empty.")

            else:
                print("Invalid selection.")

        except ValueError:
            print("Enter a valid number.")

    # Create transaction record
    transaction = {
        "id": str(uuid.uuid4()),
        "type": transaction_type,
        "description": description,
        "amount": amount,
        "category": category,
        "date": date.today().isoformat(),
    }

    transactions.append(transaction)

    try:
      save_transactions(transactions)

    except (OSError, TypeError) as error:
      print(f"\nTransaction added, but saving failed! {error}")

    else:
      print("\nTransaction recorded successfully!")

      try:
       backup_path = create_backup("automatic")
       print("Automatic backup created successfully!")

      except OSError as error:
        print(f"Warning: Transaction saved, but backup failed: {error}")
            
    
    print(f"Type: {transaction_type}")
    print(f"Description: {description}")
    print(f"Amount: GH₵{amount / 100:.2f}")
    print(f"Category: {category}")
    print(f"Date: {transaction['date']}")


def view_transactions():
    if not transactions:
        print("\nNo transactions recorded\n.")
        return

    print("\n=====All Transactions=====\n")
    for transaction in transactions:
        print(f"ID: {transaction['id']}")
        print(f"Type: {transaction['type']}")
        print(f"Description: {transaction['description']}")
        print(f"Amount: GH₵{transaction['amount'] / 100:.2f}")
        print(f"Category: {transaction['category']}")
        print(f"Date: {transaction['date']}")
        print("-" * 30)