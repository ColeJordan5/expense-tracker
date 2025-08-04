def main():
    print("Welcome to your Expense Tracker!")
    while True:
        print("\nChoose an option:")
        print("1. Add an expense")
        print("2. View summary")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def add_expense():
    amount = input("Enter amount spent: $")
    category = input("Enter category (e.g. Food, Gas, Bills): ")
    with open("expenses.txt", "a") as file:
        file.write(f"{amount},{category}\n")
    print("Expense added!")

def show_summary():
    try:
        with open("expenses.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("No expenses yet.")
        return

    total = 0
    categories = {}

    for line in lines:
        amount, category = line.strip().split(",")
        amount = float(amount)
        total += amount
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    print(f"\nTotal Spent: ${total:.2f}")
    print("By Category:")
    for cat, amt in categories.items():
        print(f"  {cat}: ${amt:.2f}")

main()
