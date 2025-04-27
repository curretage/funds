import sqlite3
from datetime import datetime

# Database Initialization
def init_db():
    conn = sqlite3.connect('expenses.db')  # Connect to the SQLite database
    cursor = conn.cursor()
    # Create expenses table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()  # Commit changes
    conn.close()   # Close connection

# Data Handling Functions
def add_expense(amount, category, description, date=datetime.today().strftime('%Y-%m-%d')):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    # Insert expense data into the database
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    # Retrieve all expenses ordered by date
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_expenses_by_period(start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    # Select expenses within the specified date range
    cursor.execute('''
        SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC
    ''', (start_date, end_date))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_expenses_by_category(category):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    # Select expenses for the specified category
    cursor.execute('''
        SELECT * FROM expenses WHERE category = ? ORDER BY date DESC
    ''', (category,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_total_by_period(start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    # Calculate total expenses in the specified date range
    cursor.execute('''
        SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?
    ''', (start_date, end_date))
    total = cursor.fetchone()[0] or 0  # Default to 0 if no expenses found
    conn.close()
    return total

def get_total_by_category(category):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    # Calculate total expenses for the specified category
    cursor.execute('''
        SELECT SUM(amount) FROM expenses WHERE category = ?
    ''', (category,))
    total = cursor.fetchone()[0] or 0  # Default to 0 if no expenses found
    conn.close()
    return total

def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    # Delete the expense with the given ID
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

# User Interface (Console)
def main():
    init_db()  # Initialize the database

    while True:  # Loop for menu
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. Show All Expenses")
        print("3. Show Expenses by Period")
        print("4. Show Expenses by Category")
        print("5. Report Total by Period")
        print("6. Report Total by Category")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount: "))  # Get amount input and convert to float
                category = input("Enter category: ")  # Get category input
                description = input("Enter description: ")  # Get description input
                date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
                if not date:  # Use current date if no date is provided
                    date = datetime.today().strftime('%Y-%m-%d')
                add_expense(amount, category, description, date)  # Add expense to database
                print("Expense added successfully!")
            except ValueError:
                print("Invalid input for amount. Please enter a number.")

        elif choice == "2":
            expenses = get_all_expenses()  # Fetch all expenses
            for expense in expenses:
                print(expense)

        elif choice == "3":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            expenses = get_expenses_by_period(start_date, end_date)  # Get expenses by date range
            for expense in expenses:
                print(expense)

        elif choice == "4":
            category = input("Enter category: ")
            expenses = get_expenses_by_category(category)  # Get expenses by category
            for expense in expenses:
                print(expense)

        elif choice == "5":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            total = get_total_by_period(start_date, end_date)  # Get total for date range
            print(f"Total expenses from {start_date} to {end_date}: {total}")

        elif choice == "6":
            category = input("Enter category: ")
            total = get_total_by_category(category)  # Get total for category
            print(f"Total expenses for {category}: {total}")

        elif choice == "7":
            print("Exiting the application.")
            break  # Exit the loop and end the program

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()  # Run the main function