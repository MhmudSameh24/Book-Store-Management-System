from tkinter import *
from tkinter import ttk
from databasesFile import main_database_conection

COLOR_PRIMARY = "#2c3e50"
COLOR_DANGER = "#e74c3c"
COLOR_BG = "#f8f9fa"

class InventoryAlertsWindow:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master, bg=COLOR_BG)
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = Frame(self.frame, bg=COLOR_PRIMARY, height=60)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="Low Stock Alerts", font=("Segoe UI", 18, "bold"), 
              fg="white", bg=COLOR_PRIMARY).pack(side=LEFT, padx=20, pady=10)
        
        Button(header, text="Logout to Home", command=self.back_to_home, 
               bg=COLOR_DANGER, fg="white", font=("Segoe UI", 10, "bold"), 
               bd=0, padx=15, cursor="hand2").pack(side=RIGHT, padx=20)

        # Dashboard container
        self.dashboard = Frame(self.frame, bg=COLOR_BG, padx=20, pady=20)
        self.dashboard.pack(fill=BOTH, expand=True)

        Label(self.dashboard, text="Books with 10 or fewer copies in stock:", 
              font=("Segoe UI", 14), bg=COLOR_BG, fg="#333").pack(anchor=W, pady=(0,10))

        # Table
        columns = ("id", "title", "author", "price", "stock")
        self.tree = ttk.Treeview(self.dashboard, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("price", text="Price")
        self.tree.heading("stock", text="Stock")

        self.tree.column("id", width=50)
        self.tree.column("title", width=250)
        self.tree.column("author", width=150)
        self.tree.column("price", width=80)
        self.tree.column("stock", width=80)
        
        self.tree.tag_configure('danger', background='#ffcccc')

        self.tree.pack(fill=BOTH, expand=True)

        Button(self.dashboard, text="Refresh List", command=self.load_data,
               bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 12, "bold")).pack(pady=15)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        books = main_database_conection.free_execute("SELECT book_id, title, author, price, quantity FROM Books WHERE quantity <= 10 ORDER BY quantity ASC")
        
        if books:
            for book in books:
                tags = ('danger',) if book['quantity'] == 0 else ()
                self.tree.insert("", "end", values=(
                    book['book_id'], 
                    book['title'], 
                    book['author'], 
                    f"${book['price']:.2f}", 
                    book['quantity']
                ), tags=tags)
        else:
            self.tree.insert("", "end", values=("-", "All stock levels are healthy!", "-", "-", "-"))

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)
        self.load_data()

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()
