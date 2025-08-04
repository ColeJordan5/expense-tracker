import csv
from datetime import datetime

FILENAME = "expenses.csv"

def add_expense():
    category = input("Enter expense category (e.g., food, rent): ").strip()
    amount = input("Enter amount: ").strip()

    # Validate amount
    try:
        amount = float(amount)
    except ValueError:
        print("Amount must be a number.")
        return

    # Get today's date in YYYY-MM-DD format
    today = datetime.today().strftime('%Y-%m-%d')

    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([today, category, amount])
    
    print(f"✅ Expense added: {category} - ${amount} on {today}")

def view_expenses():
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            print("\n📄 All Expenses:")
            print("DATE        | CATEGORY       | AMOUNT")
            print("--------------------------------------")
            total = 0
            for row in reader:
                date, category, amount = row
                print(f"{date} | {category:<14} | ${amount}")
                total += float(amount)
            print(f"\n💰 Total Spent: ${total:.2f}")
    except FileNotFoundError:
        print("No expenses found yet.")

def view_monthly_summary():
    month_input = input("Enter month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month_input, "%Y-%m")
    except ValueError:
        print("Invalid format. Use YYYY-MM (e.g., 2025-08).")
        return

    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            print(f"\n📊 Summary for {month_input}:")
            total = 0
            for row in reader:
                date, category, amount = row
                if date.startswith(month_input):
                    print(f"{date} | {category:<14} | ${amount}")
                    total += float(amount)
            print(f"\n📅 Total Spent in {month_input}: ${total:.2f}")
    except FileNotFoundError:
        print("No expenses recorded yet.")

def show_menu():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Monthly Summary")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_monthly_summary()
        elif choice == "4":
            print("👋 Exiting. See you later!")
            break
        else:
            print("Invalid choice. Try 1, 2, 3, or 4.")

if __name__ == "__main__":
    show_menu()
