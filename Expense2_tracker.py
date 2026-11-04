import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# File to store expenses
FILE_NAME = "expenses.csv"

# Initialize CSV file if not exists
def init_file():
    try:
        with open(FILE_NAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("650x500")
        
        init_file()
        self.setup_ui()
        self.view_expenses()

    def setup_ui(self):
        # Input Frame
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.cat_entry = tk.Entry(input_frame)
        self.cat_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Amount (₹):").grid(row=0, column=2, padx=5, pady=5)
        self.amt_entry = tk.Entry(input_frame)
        self.amt_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Buttons Frame
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="1️⃣ Add Expense", bg="#4CAF50", fg="white", command=self.add_expense).pack(side="left", padx=10)
        tk.Button(btn_frame, text="3️⃣ Summary by Category", bg="#2196F3", fg="white", command=self.summary_by_category).pack(side="left", padx=10)
        tk.Button(btn_frame, text="4️⃣ Exit", bg="#f44336", fg="white", command=self.root.quit).pack(side="right", padx=10)

        # Table Frame (View Expenses)
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(table_frame, text="2️⃣ View Expenses", font=("Arial", 10, "bold")).pack(anchor="w")

        columns = ("Date", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col != "Description" else 220)
            
        self.tree.pack(fill="both", expand=True)

    # Add a new expense (Logic kept same)
    def add_expense(self):
        category = self.cat_entry.get().strip()
        amount_text = self.amt_entry.get().strip()
        description = self.desc_entry.get().strip()

        if not category or not amount_text:
            messagebox.showwarning("Input Error", "Category and Amount are required!")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Input Error", "❌ Amount must be a number!")
            return

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category.lower(), amount, description])
            
        self.cat_entry.delete(0, tk.END)
        self.amt_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        
        self.view_expenses()
        messagebox.showinfo("Success", "✅ Expense added successfully!")

    # View all expenses (Logic kept same)
    def view_expenses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            with open(FILE_NAME, "r") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                for row in reader:
                    self.tree.insert("", tk.END, values=row)
        except FileNotFoundError:
            pass

    # Get summary by category (Logic kept same)
    def summary_by_category(self):
        categories = {}
        try:
            with open(FILE_NAME, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row["Category"].lower()
                    amount = float(row["Amount"])
                    categories[category] = categories.get(category, 0) + amount
        except FileNotFoundError:
            return

        if not categories:
            messagebox.showinfo("Summary", "No expenses to show.")
            return

        summary_text = "📊 Expense Summary by Category:\n"
        summary_text += "-" * 40 + "\n"
        summary_text += f"{'Category':<15}{'Total (₹)':>15}\n"
        summary_text += "-" * 40 + "\n"
        
        for category, total in categories.items():
            summary_text += f"{category.capitalize():<15}{total:>15.2f}\n"
            
        summary_text += "-" * 40

        messagebox.showinfo("Summary", summary_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
