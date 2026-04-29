from tkinter import *
from tkinter import ttk, messagebox
from order import Order
from classesFile import manage_book_conection, manage_user_conection, manage_bill_conection
from databasesFile import main_database_conection
import json
import os

# Custom Styles
COLOR_PRIMARY = "#2c3e50"
COLOR_ACCENT = "#3498db"
COLOR_SUCCESS = "#27ae60"
COLOR_DANGER = "#e74c3c"
COLOR_BG = "#f8f9fa"

class ManageOrders:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        
        # Logic Objects
        self.order_logic = Order(main_database_conection)
        self.bill_logic = manage_bill_conection
        
        self.frame = Frame(master, bg=COLOR_BG)
        self.setup_ui()

    def setup_ui(self):
        # --- Navigation Header ---
        header = Frame(self.frame, bg=COLOR_PRIMARY, height=60)
        header.pack(side=TOP, fill=X)
        
        store_name = "PRO Bookstore POS"
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    name = data.get("name", "").strip()
                    if name: store_name = name
            except: pass
        
        Label(header, text=store_name, font=("Segoe UI", 18, "bold"), 
              fg="white", bg=COLOR_PRIMARY).pack(side=LEFT, padx=20, pady=10)
        
        Button(header, text="Logout to Home", command=self.back_to_home, 
               bg=COLOR_DANGER, fg="white", font=("Segoe UI", 10, "bold"), 
               bd=0, padx=15, cursor="hand2").pack(side=RIGHT, padx=20)

        # --- Main Tabs (Notebook) ---
        self.tabs = ttk.Notebook(self.frame)
        self.tabs.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # TAB 1: Checkout
        self.tab_checkout = Frame(self.tabs, bg=COLOR_BG)
        self.tabs.add(self.tab_checkout, text="  New Transaction  ")
        self.build_checkout_tab()

        # TAB 2: History
        self.tab_history = Frame(self.tabs, bg=COLOR_BG)
        self.tabs.add(self.tab_history, text="  Bill History  ")
        self.build_history_tab()

    def build_checkout_tab(self):
        # Container for Checkout
        container = Frame(self.tab_checkout, bg=COLOR_BG)
        container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # LEFT: Inventory Browser
        left_side = LabelFrame(container, text=" Inventory ", bg="white", padx=10, pady=10)
        left_side.pack(side=LEFT, fill=BOTH, expand=True)

        # Search Bar
        search_frame = Frame(left_side, bg="white")
        search_frame.pack(fill=X, pady=(0, 10))
        Label(search_frame, text="Search:", bg="white").pack(side=LEFT)
        self.search_entry = Entry(search_frame)
        self.search_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_inventory)

        # Inventory Table
        self.inv_tree = ttk.Treeview(left_side, columns=("id", "title", "price", "stock"), show="headings")
        for col in [("id", "ID", 40), ("title", "Title", 150), ("price", "Price", 70), ("stock", "Stock", 60)]:
            self.inv_tree.heading(col[0], text=col[1])
            self.inv_tree.column(col[0], width=col[2])
        self.inv_tree.pack(fill=BOTH, expand=True)
        self.inv_tree.bind("<<TreeviewSelect>>", self.on_inventory_click)

        # RIGHT: Cart & Controls
        right_side = Frame(container, bg=COLOR_BG, width=350)
        right_side.pack(side=LEFT, fill=Y, padx=(10, 0))

        # Item Config
        config_frame = LabelFrame(right_side, text=" Selection ", bg="white", padx=10, pady=10)
        config_frame.pack(fill=X)

        Label(config_frame, text="ID:", bg="white").grid(row=0, column=0, sticky=W)
        self.id_var = StringVar()
        Entry(config_frame, textvariable=self.id_var, state="readonly").grid(row=0, column=1, sticky=EW, padx=5)

        Label(config_frame, text="Qty:", bg="white").grid(row=1, column=0, sticky=W, pady=5)
        self.qty_entry = Entry(config_frame)
        self.qty_entry.insert(0, "1")
        self.qty_entry.grid(row=1, column=1, sticky=EW, padx=5)

        Button(config_frame, text="Add to Cart", bg=COLOR_ACCENT, fg="white", 
               command=self.add_item, font=("Segoe UI", 9, "bold")).grid(row=2, column=0, columnspan=2, sticky=EW, pady=5)

        # Cart Table
        cart_frame = LabelFrame(right_side, text=" Your Cart ", bg="white", padx=10, pady=10)
        cart_frame.pack(fill=BOTH, expand=True, pady=10)

        self.cart_tree = ttk.Treeview(cart_frame, columns=("id", "title", "qty", "total"), show="headings", displaycolumns=("title", "qty", "total"))
        self.cart_tree.heading("title", text="Item")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("total", text="Total")
        self.cart_tree.column("qty", width=40)
        self.cart_tree.column("total", width=70)
        self.cart_tree.pack(fill=BOTH, expand=True)

        Button(cart_frame, text="Remove Selected", command=self.remove_from_cart, 
               bg=COLOR_DANGER, fg="white", font=("Segoe UI", 8)).pack(fill=X, pady=5)

        # Finalize
        checkout_box = Frame(right_side, bg="white", padx=10, pady=10, highlightbackground="#ddd", highlightthickness=1)
        checkout_box.pack(fill=X)

        Label(checkout_box, text="Customer Email:", bg="white").pack(anchor=W)
        self.email_entry = Entry(checkout_box)
        self.email_entry.pack(fill=X, pady=5)

        Button(checkout_box, text="FINALIZE SALE", bg=COLOR_SUCCESS, fg="white", 
               font=("Segoe UI", 12, "bold"), command=self.complete_sale).pack(fill=X)

    def build_history_tab(self):
        """Creates a view for past bills."""
        frame = Frame(self.tab_history, bg="white", padx=20, pady=20)
        frame.pack(fill=BOTH, expand=True)
        
        Label(frame, text="Recent Transactions", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor=W)
        
        self.history_tree = ttk.Treeview(frame, columns=("id", "user", "email", "total", "date"), show="headings")
        self.history_tree.heading("id", text="Bill #")
        self.history_tree.heading("user", text="Customer ID")
        self.history_tree.heading("email", text="Email")
        self.history_tree.heading("total", text="Total Paid")
        self.history_tree.heading("date", text="Date")
        self.history_tree.pack(fill=BOTH, expand=True, pady=10)
        
        Button(frame, text="Refresh History", command=self.load_history).pack(side=RIGHT)

    # --- LOGIC METHODS ---

    def load_inventory(self, search_text=""):
        for item in self.inv_tree.get_children(): self.inv_tree.delete(item)
        
        books = manage_book_conection.get_all_books()
        
        found_any = False
        for b in books:
            if search_text.lower() in b.get_title().lower():
                self.inv_tree.insert("", "end", values=(
                    b.get_book_id(), b.get_title(), f"${b.get_price():.2f}", b.get_quantity()
                ))
                found_any = True
                
        if not found_any:
            self.inv_tree.insert("", "end", values=("-", "No books available", "-", "-"))

    def on_inventory_click(self, event):
        selected = self.inv_tree.selection()
        if selected:
            data = self.inv_tree.item(selected[0])["values"]
            if str(data[0]) == "-": return
            self.id_var.set(data[0])

    def filter_inventory(self, event):
        self.load_inventory(self.search_entry.get())

    def add_item(self):
        try:
            bid = int(self.id_var.get())
            qty = int(self.qty_entry.get())
            self.order_logic.add_book(bid, qty)
            self.update_cart_ui()
        except:
            messagebox.showerror("Error", "Select a book and enter a valid quantity.")

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected: return
        item = self.cart_tree.item(selected[0])["values"]
        if str(item[0]) == "-": return
        book_id = item[0]
        qty = item[2]
        self.order_logic.remove_book(book_id, qty)
        self.update_cart_ui()

    def update_cart_ui(self):
        for item in self.cart_tree.get_children(): self.cart_tree.delete(item)
        books = self.order_logic.get_ordered_books()
        if books:
            for b in books:
                qty = self.order_logic.books[b.get_book_id()]
                self.cart_tree.insert("", "end", values=(b.get_book_id(), b.get_title(), qty, f"${b.get_price()*qty:.2f}"))
        else:
            self.cart_tree.insert("", "end", values=("-", "Cart is empty", "-", "-"))

    def complete_sale(self):
        if not self.order_logic.books:
            messagebox.showwarning("Empty Cart", "Your cart is empty. Please add items before finalizing the sale.")
            return
            
        email = self.email_entry.get()
        if not email or "@" not in email:
            messagebox.showwarning("Input", "Enter a valid email.")
            return

        if not manage_user_conection.user_exists(email):
            messagebox.showerror("Error", "User email not found in database.")
            return

        if self.order_logic.complete_purchase(email):
            bill_text = self.order_logic.create_bill()
            messagebox.showinfo("BILL GENERATED", bill_text)
            self.order_logic.books.clear() # Clear for next order
            self.update_cart_ui()
            self.load_inventory() # Update stock levels in UI
            
            # Clear fields
            self.id_var.set("")
            self.qty_entry.delete(0, END)
            self.qty_entry.insert(0, "1")
            self.email_entry.delete(0, END)
        else:
            messagebox.showerror("Failed", "Transaction failed. Check stock levels.")

    def load_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        bills = main_database_conection.free_execute('''
            SELECT b.bill_id, u.email, b.total, b.date_time, b.user_id
            FROM Bills b
            JOIN Users u ON b.user_id = u.user_id
            ORDER BY b.bill_id DESC
        ''')
        
        if bills:
            for b in bills:
                self.history_tree.insert("", "end", values=(b["bill_id"], b["user_id"], b["email"], f"${float(b['total']):.2f}", b["date_time"]))
        else:
            self.history_tree.insert("", "end", values=("-", "-", "No history available", "-", "-"))

    # --- WINDOW MANAGEMENT ---
    def display(self):
        self.frame.pack(fill=BOTH, expand=True)
        self.load_inventory()
        self.load_history()

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()