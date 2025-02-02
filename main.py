import json
import os
from datetime import datetime

data_file = 'expenses.json'

# Load data from the file or return empty data if the file doesn't exist
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return {"expenses": [], "budget": {}}

# Save updated data back to the file
def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

# Add a new expense to the data
def add_expense(data, description, amount, category=None):
    expense = {
        "index": len(data['expenses']),
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime('%Y-%m-%d'),
        "category": category
    }
    data['expenses'].append(expense)
    save_data(data)

# Update an existing expense by index
def update_expense(data, index, description, amount, category=None):
    if index < len(data['expenses']):
        data['expenses'][index] = {
            "index": index,
            "description": description,
            "amount": amount,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "category": category
        }
        save_data(data)
    else:
        print("Invalid index.")

# Delete an expense by index and reindex the list
def delete_expense(data, index):
    if index < len(data['expenses']):
        del data['expenses'][index]
        for i, expense in enumerate(data['expenses']):
            # Reindex remaining expenses
            expense['index'] = i
        save_data(data)
    else:
        print("Invalid index.")

# View all expenses
def view_expenses(data):
    for expense in data['expenses']:
        print(f"Index: {expense['index']} - {expense['description']} - {expense['amount']} - {expense['date']} - {expense['category']}")

# Show total expenses
def view_summary(data):
    total = sum(expense['amount'] for expense in data['expenses'])
    print(f"Total Expenses: {total}")

# Show total expenses for a specific month
def view_month_summary(data, month):
    month_expenses = [expense for expense in data['expenses'] if expense['date'].startswith(f'{datetime.now().year}-{month:02d}')]
    total = sum(expense['amount'] for expense in month_expenses)
    print(f"Total Expenses for {datetime.now().year}-{month:02d}: {total}")

# Set budget for a specific month
def set_budget(data, month, budget):
    data['budget'][month] = budget
    save_data(data)

# Check if the current month's expenses exceed the budget
def check_budget(data):
    month = datetime.now().month
    total = sum(expense['amount'] for expense in data['expenses'] if expense['date'].startswith(f'{datetime.now().year}-{month:02d}'))
    if month in data['budget'] and total > data['budget'][month]:
        print(f"Warning: You've exceeded your budget of {data['budget'][month]} with a total of {total}.")
    else:
        print(f"Your expenses for this month are within the budget.")

# Export expenses to a CSV file
def export_to_csv(data):
    import csv
    with open('expenses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Description", "Amount", "Date", "Category"])
        for expense in data['expenses']:
            writer.writerow([expense['description'], expense['amount'], expense['date'], expense['category']])

# Main loop for user interaction
def main():
    data = load_data()

    while True:
        print("\n1. Add Expense")
        print("2. Update Expense")
        print("3. Delete Expense")
        print("4. View Expenses")
        print("5. View Summary")
        print("6. View Monthly Summary")
        print("7. Set Budget")
        print("8. Check Budget")
        print("9. Export to CSV")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            category = input("Enter category (optional): ")
            add_expense(data, description, amount, category)

        elif choice == '2':
            index = int(input("Enter the index of the expense to update: "))
            description = input("Enter new description: ")
            amount = float(input("Enter new amount: "))
            category = input("Enter new category (optional): ")
            update_expense(data, index, description, amount, category)

        elif choice == '3':
            index = int(input("Enter the index of the expense to delete: "))
            delete_expense(data, index)

        elif choice == '4':
            view_expenses(data)

        elif choice == '5':
            view_summary(data)

        elif choice == '6':
            month = int(input("Enter month (1-12): "))
            view_month_summary(data, month)

        elif choice == '7':
            month = int(input("Enter month (1-12): "))
            budget = float(input("Enter budget amount: "))
            set_budget(data, month, budget)

        elif choice == '8':
            check_budget(data)

        elif choice == '9':
            export_to_csv(data)

        elif choice == '0':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
