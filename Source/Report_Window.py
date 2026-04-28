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

        # Top Section: KPI Cards
        cards_frame = Frame(self.dashboard, bg=COLOR_BG)
        cards_frame.pack(fill=X, pady=(0, 20))

        # Labels for stats
        self.total_revenue_var = StringVar(value="$0.00")
        self.total_orders_var = StringVar(value="0")
        self.total_users_var = StringVar(value="0")
        self.total_books_var = StringVar(value="0")
        self.books_sold_var = StringVar(value="0")
        self.best_seller_var = StringVar(value="N/A")

        self.create_stat_card(cards_frame, "Total Revenue", self.total_revenue_var, 0, 0, "#27ae60")
        self.create_stat_card(cards_frame, "Total Orders", self.total_orders_var, 0, 1, "#2980b9")
        self.create_stat_card(cards_frame, "Registered Users", self.total_users_var, 0, 2, "#8e44ad")
        
        self.create_stat_card(cards_frame, "Books in Inventory", self.total_books_var, 1, 0, "#f39c12")
        self.create_stat_card(cards_frame, "Total Books Sold", self.books_sold_var, 1, 1, "#e67e22")
        self.create_stat_card(cards_frame, "Best Selling Book", self.best_seller_var, 1, 2, "#c0392b")

        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)

        # Bottom Section: Recent Transactions
        table_frame = Frame(self.dashboard, bg=COLOR_BG)
        table_frame.pack(fill=BOTH, expand=True)

        header_frame = Frame(table_frame, bg=COLOR_BG)
        header_frame.pack(fill=X, pady=(0, 10))
        Label(header_frame, text="Recent Transactions", font=("Segoe UI", 16, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY).pack(side=LEFT)
        Button(header_frame, text="Refresh Data", command=self.load_data,
               bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"), cursor="hand2").pack(side=RIGHT)

        # Treeview
        columns = ("bill_id", "customer", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        self.tree.heading("bill_id", text="Bill ID")
        self.tree.heading("customer", text="Customer Email")
        self.tree.heading("total", text="Total Amount")
        
        self.tree.column("bill_id", width=100, anchor=CENTER)
        self.tree.column("customer", width=300)
        self.tree.column("total", width=150, anchor=CENTER)

        self.tree.pack(fill=BOTH, expand=True)

    def create_stat_card(self, parent, title, var, row, col, color):
        card = Frame(parent, bg="white", padx=15, pady=15, highlightbackground=color, highlightthickness=2)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        Label(card, text=title, font=("Segoe UI", 12), bg="white", fg="#7f8c8d").pack()
        Label(card, textvariable=var, font=("Segoe UI", 18, "bold"), bg="white", fg=color).pack(pady=(5,0))

    def load_data(self):
        # Total Revenue & Orders
        bills = main_database_conection.free_execute("SELECT total FROM Bills")
        total_rev = sum([float(b["total"]) for b in bills]) if bills else 0.0
        total_orders = len(bills) if bills else 0
        
        # Total Users
        users = main_database_conection.free_execute("SELECT count(*) as count FROM Users")
        total_users = users[0]["count"] if users else 0
        
        # Total Books
        books = main_database_conection.free_execute("SELECT sum(quantity) as count FROM Books")
        total_books = books[0]["count"] if books and books[0]["count"] else 0

        # Total Books Sold
        sold = main_database_conection.free_execute("SELECT sum(quantity) as count FROM BookOrder")
        total_sold = sold[0]["count"] if sold and sold[0]["count"] else 0

        # Best Selling Book
        best = main_database_conection.free_execute('''
            SELECT b.title, SUM(o.quantity) as sold_qty 
            FROM BookOrder o 
            JOIN Books b ON o.book_id = b.book_id 
            GROUP BY o.book_id 
            ORDER BY sold_qty DESC 
            LIMIT 1
        ''')
        best_seller = best[0]["title"] if best else "None"

        # Update Variables
        self.total_revenue_var.set(f"${total_rev:.2f}")
        self.total_orders_var.set(str(total_orders))
        self.total_users_var.set(str(total_users))
        self.total_books_var.set(str(total_books))
        self.books_sold_var.set(str(total_sold))
        self.best_seller_var.set(str(best_seller))

        # Recent Transactions Table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        recent = main_database_conection.free_execute('''
            SELECT b.bill_id, u.email, b.total
            FROM Bills b
            JOIN Users u ON b.user_id = u.user_id
            ORDER BY b.bill_id DESC
            LIMIT 10
        ''')
        
        if recent:
            for r in recent:
                self.tree.insert("", "end", values=(r["bill_id"], r["email"], f"${float(r['total']):.2f}"))

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)
        self.load_data()

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()
