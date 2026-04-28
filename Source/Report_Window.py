from tkinter import *
from tkinter import ttk, messagebox
from databasesFile import main_database_conection

COLOR_PRIMARY = "#2c3e50"
COLOR_ACCENT = "#3498db"
COLOR_BG = "#f8f9fa"

class ReportWindow:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master, bg=COLOR_BG)
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = Frame(self.frame, bg=COLOR_PRIMARY, height=60)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="Business Reports", font=("Segoe UI", 18, "bold"), 
              fg="white", bg=COLOR_PRIMARY).pack(side=LEFT, padx=20, pady=10)
        
        Button(header, text="Logout to Home", command=self.back_to_home, 
               bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), 
               bd=0, padx=15, cursor="hand2").pack(side=RIGHT, padx=20)

        # Dashboard container
        self.dashboard = Frame(self.frame, bg=COLOR_BG)
        self.dashboard.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Labels for stats
        self.total_revenue_var = StringVar(value="$0.00")
        self.total_orders_var = StringVar(value="0")
        self.total_users_var = StringVar(value="0")
        self.total_books_var = StringVar(value="0")

        self.create_stat_card("Total Revenue", self.total_revenue_var, 0, 0, "#27ae60")
        self.create_stat_card("Total Orders", self.total_orders_var, 0, 1, "#2980b9")
        self.create_stat_card("Registered Users", self.total_users_var, 1, 0, "#8e44ad")
        self.create_stat_card("Books in Inventory", self.total_books_var, 1, 1, "#f39c12")

        Button(self.dashboard, text="Refresh Data", command=self.load_data,
               bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, columnspan=2, pady=20)

        # Ensure grid expansion
        self.dashboard.grid_columnconfigure(0, weight=1)
        self.dashboard.grid_columnconfigure(1, weight=1)

    def create_stat_card(self, title, var, row, col, color):
        card = Frame(self.dashboard, bg="white", padx=20, pady=20, highlightbackground=color, highlightthickness=2)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        Label(card, text=title, font=("Segoe UI", 14), bg="white", fg="#7f8c8d").pack()
        Label(card, textvariable=var, font=("Segoe UI", 24, "bold"), bg="white", fg=color).pack(pady=(10,0))

    def load_data(self):
        # Get Total Revenue & Orders
        bills = main_database_conection.free_execute("SELECT total FROM Bills")
        total_rev = sum([float(b["total"]) for b in bills]) if bills else 0.0
        total_orders = len(bills) if bills else 0
        
        # Get Total Users
        users = main_database_conection.free_execute("SELECT count(*) as count FROM Users")
        total_users = users[0]["count"] if users else 0
        
        # Get Total Books
        books = main_database_conection.free_execute("SELECT sum(quantity) as count FROM Books")
        total_books = books[0]["count"] if books and books[0]["count"] else 0

        self.total_revenue_var.set(f"${total_rev:.2f}")
        self.total_orders_var.set(str(total_orders))
        self.total_users_var.set(str(total_users))
        self.total_books_var.set(str(total_books))

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)
        self.load_data()

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()
