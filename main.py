from modules.transactions import transactions
from modules.data_manager import load_transactions
from modules.transactions import add_transaction, view_transactions
from modules.calculations import calculate_balance
from modules.backups import manual_backup, view_backups, restore_backup

def main():
    try:
      saved_transactions = load_transactions()
      transactions.extend(saved_transactions)

      print(f"Loaded {len(transactions)} transactions.")

    except (ValueError, OSError) as error:
      print(f"Unable to load transaction data: {error}")
      return

    while True:
      print("\n===Main Menu===\n")
      print("1. Add Transaction")
      print("2. View All Transactions")
      print("3. View Financial Statement")
      print("4. Create Manual Backup")
      print("5. View Backup History")
      print("6. Restore Backup")
      print("7. Exit")

      choice = input("Enter your choice: ")

      if choice == "1":
          add_transaction()

      elif choice == "2":
          view_transactions()

      elif choice == "3":
          calculate_balance()

      elif choice == "4":
         manual_backup()
         
      elif choice == "5":
         view_backups()

      elif choice == "6":
         
         backups = view_backups()

         if not backups:
            continue

        # Ask the user which backup to restore
         try:
             selection = int(input("\nSelect backup number to restore: "))

             if selection < 1 or selection > len(backups):
                print("Invalid backup selection.")
                continue

             selected_backup = backups[selection - 1]

            # Restore the selected backup
             restored_transactions = restore_backup  (selected_backup)

            # Update the application's transaction list
             transactions[:] = restored_transactions

         except ValueError as error:
                print(f"Unable to restore backup: {error}")

         except OSError as error:
                print(f"File operation failed: {error}")

      elif choice == "7":
        print("\nThank you for using this!!!")
        break

      else:
        print("\nInvalid selection. Select a value from 1-7.")

if __name__ == "__main__":
    main()
