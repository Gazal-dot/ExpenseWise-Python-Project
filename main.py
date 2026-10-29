"""
ExpenseWise - Personal Expense Tracker
Built with core Python and JSON file storage.
Run: python main.py
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

DATA_FILE = Path(__file__).with_name("expenses.json")
BUDGET_FILE = Path(__file__).with_name("budget.json")
DATE_FORMAT = "%Y-%m-%d"


def load_json(path, default):
    """Load JSON data, returning a safe default if the file doesn't exist."""
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not read {path.name}; starting with default data.")
        return default


def save_json(path, data):
    """Save data as readable JSON."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_expenses():
    return load_json(DATA_FILE, [])


def add_expense():
    print("\n--- Add Expense ---")
    title = input("Expense title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    category = input("Category (Food/Travel/Study/Bills/Shopping/Other): ").strip().title()
    if not category:
        category = "Other"

    try:
        amount = float(input("Amount (₹): ").strip())
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number for amount.")
        return

    date_text = input(f"Date (YYYY-MM-DD, Enter for today [{datetime.today().date()}]): ").strip()
    if not date_text:
        date_text = datetime.today().strftime(DATE_FORMAT)
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    expenses = load_expenses()
    expense = {
        "id": max((item.get("id", 0) for item in expenses), default=0) + 1,
        "title": title,
        "category": category,
        "amount": round(amount, 2),
        "date": date_text,
    }
    expenses.append(expense)
    save_json(DATA_FILE, expenses)
    print(f"Saved! ₹{amount:.2f} recorded for {title}.")
    check_budget(date_text[:7], expenses)


def view_expenses():
    expenses = sorted(load_expenses(), key=lambda item: item.get("date", ""), reverse=True)
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses yet. Add your first expense!")
        return
    print(f"{'ID':<5}{'Date':<13}{'Category':<15}{'Title':<25}{'Amount (₹)':>12}")
    print("-" * 70)
    for item in expenses:
        print(f"{item.get('id', '-'):<5}{item.get('date', '-'):<13}"
              f"{item.get('category', 'Other')[:14]:<15}"
              f"{item.get('title', '-')[:24]:<25}{item.get('amount', 0):>12.2f}")
    print("-" * 70)
    print(f"Total: ₹{sum(float(x.get('amount', 0)) for x in expenses):.2f}")


def monthly_report():
    expenses = load_expenses()
    month = input("Enter month (YYYY-MM, e.g. 2026-10): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    selected = [x for x in expenses if x.get("date", "").startswith(month)]
    print(f"\n--- Report for {month} ---")
    if not selected:
        print("No expenses found for this month.")
        return

    total = sum(float(x.get("amount", 0)) for x in selected)
    categories = defaultdict(float)
    for item in selected:
        categories[item.get("category", "Other")] += float(item.get("amount", 0))

    print(f"Number of expenses: {len(selected)}")
    print(f"Total spent: ₹{total:.2f}")
    print("\nSpending by category:")
    for category, amount in sorted(categories.items(), key=lambda pair: pair[1], reverse=True):
        percent = (amount / total * 100) if total else 0
        bar = "#" * int(percent // 5)
        print(f"{category:<15} ₹{amount:>9.2f}  {percent:5.1f}% {bar}")

    report_path = Path(__file__).with_name(f"report_{month}.txt")
    with report_path.open("w", encoding="utf-8") as file:
        file.write(f"ExpenseWise Monthly Report: {month}\n")
        file.write(f"Total spent: ₹{total:.2f}\n\n")
        for category, amount in sorted(categories.items(), key=lambda pair: pair[1], reverse=True):
            file.write(f"{category}: ₹{amount:.2f}\n")
    print(f"\nReport exported to {report_path.name}")


def set_budget():
    print("\n--- Set Monthly Budget ---")
    try:
        amount = float(input("Enter your monthly budget (₹): ").strip())
        if amount <= 0:
            print("Budget must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    save_json(BUDGET_FILE, {"monthly_budget": round(amount, 2)})
    print(f"Monthly budget set to ₹{amount:.2f}.")
    month = datetime.today().strftime("%Y-%m")
    check_budget(month, load_expenses())


def check_budget(month, expenses=None):
    budget_data = load_json(BUDGET_FILE, {})
    budget = budget_data.get("monthly_budget")
    if not budget:
        return
    if expenses is None:
        expenses = load_expenses()
    spent = sum(float(x.get("amount", 0)) for x in expenses if x.get("date", "").startswith(month))
    remaining = float(budget) - spent
    print(f"Budget status ({month}): ₹{spent:.2f} spent / ₹{float(budget):.2f} budget.")
    if remaining < 0:
        print(f"ALERT: Budget exceeded by ₹{abs(remaining):.2f}!")
    elif remaining <= float(budget) * 0.2:
        print(f"Warning: Only ₹{remaining:.2f} budget remaining.")
    else:
        print(f"Remaining budget: ₹{remaining:.2f}")


def delete_expense():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to delete.")
        return
    view_expenses()
    try:
        expense_id = int(input("Enter the ID to delete: ").strip())
    except ValueError:
        print("Please enter a valid ID.")
        return
    updated = [item for item in expenses if item.get("id") != expense_id]
    if len(updated) == len(expenses):
        print("No expense found with that ID.")
        return
    save_json(DATA_FILE, updated)
    print(f"Expense #{expense_id} deleted.")


def main():
    while True:
        print("\n" + "=" * 38)
        print("          EXPENSEWISE")
        print("    Personal Expense Tracker")
        print("=" * 38)
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Monthly report")
        print("4. Set monthly budget")
        print("5. Delete an expense")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_report()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Thanks for using ExpenseWise. Stay within budget!")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
