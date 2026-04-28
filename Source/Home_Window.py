from tkinter import *
import json
import os
from Validation import Validation
from tkinter import ttk, messagebox
from Mange_Book_Window import ManageBooks
from Manage_Users_Window import ManageUsers
from Manage_Orders_Window import ManageOrders
from Report_Window import ReportWindow
from Inventory_Alerts_Window import InventoryAlertsWindow


class BookstoreApp:
    def __init__(self, root):
        self.root = root
        
        self.store_name = "Bookstore Management System"
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    name = data.get("name", "").strip()
                    if name:
                        self.store_name = name
            except:
                pass

        self.root.title(self.store_name)
        self.root.geometry("800x500")
        # icon = PhotoImage(file="Icon.png")
        # self.root.iconphoto(False, icon)
        self.create_main_ui()
        self.home_frame.grid_rowconfigure(0, weight=3)
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)
        self.home_frame.grid_rowconfigure(3, weight=1)
        self.home_frame.grid_rowconfigure(4, weight=1)
        self.home_frame.grid_rowconfigure(5, weight=1)
        self.home_frame.grid_rowconfigure(6, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(2, weight=1)

    def create_main_ui(self):
        self.home_frame = Frame(self.root)

        lab1 = Label(
            self.home_frame,
            text=self.store_name,
            font=("Arial", 35),
            fg="#2c3e50",
        )
        lab1.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="we")

        btn1 = Button(
            self.home_frame,
            text="Manage Books",
            command=self.open_manage_books,
            width=35,
            height=2,
            bg="#3498db",
            font=("Arial", 20),
            activebackground="#2980b9",
            activeforeground="#ffffff",
        )
        btn1.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        btn2 = Button(
            self.home_frame,
            text="Manage Users",
            command=self.open_manage_users,
            width=35,
            height=2,
            bg="#3498db",
            font=("Arial", 20),
            activebackground="#2980b9",
            activeforeground="#ffffff",
        )
        btn2.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        btn3 = Button(
            self.home_frame,
            text="Manage Orders",
            command=self.open_manage_orders,
            width=35,
            height=2,
            bg="#3498db",
            font=("Arial", 20),
            activebackground="#2980b9",
            activeforeground="#ffffff",
        )
        btn3.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

        btn4 = Button(
            self.home_frame,
            text="Business Reports",
            command=self.open_reports,
            width=35,
            height=2,
            bg="#3498db",
            font=("Arial", 20),
            activebackground="#2980b9",
            activeforeground="#ffffff",
        )
        btn4.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

        btn5 = Button(
            self.home_frame,
            text="Low Stock Alerts",
            command=self.open_inventory_alerts,
            width=35,
            height=2,
            bg="#3498db",
            font=("Arial", 20),
            activebackground="#2980b9",
            activeforeground="#ffffff",
        )
        btn5.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

        self.home_frame.pack(fill=BOTH, expand=True)

    def open_manage_books(self):
        self.home_frame.pack_forget()
        self.manage_books = ManageBooks(self.root, self.show_home)
        self.manage_books.display()

    def open_manage_users(self):
        self.home_frame.pack_forget()
        self.manage_users = ManageUsers(self.root, self.show_home)
        self.manage_users.display()

    def open_manage_orders(self):
        self.home_frame.pack_forget()
        self.manage_orders = ManageOrders(self.root, self.show_home)
        self.manage_orders.display()

    def open_reports(self):
        self.home_frame.pack_forget()
        self.report_window = ReportWindow(self.root, self.show_home)
        self.report_window.display()

    def open_inventory_alerts(self):
        self.home_frame.pack_forget()
        self.inventory_alerts_window = InventoryAlertsWindow(self.root, self.show_home)
        self.inventory_alerts_window.display()

    def show_home(self):
        if hasattr(self, "manage_books"):
            self.manage_books.hide()
        if hasattr(self, "manage_users"):
            self.manage_users.hide()
        if hasattr(self, "manage_orders"):
            self.manage_orders.hide()
        if hasattr(self, "report_window"):
            self.report_window.hide()
        if hasattr(self, "inventory_alerts_window"):
            self.inventory_alerts_window.hide()

        self.home_frame.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    app = BookstoreApp(root)
    root.mainloop()
