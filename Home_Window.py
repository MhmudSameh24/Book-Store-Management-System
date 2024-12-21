from tkinter import *
from tkinter import ttk, messagebox
from Validation import Validation
from Mange_Book_Window import ManageBooks
from Manage_Users_Window import ManageUsers
from Manage_Orders_Window import ManageOrders


class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore Management System")
        self.root.geometry("800x500")
        self.create_main_ui()
        self.home_frame.grid_rowconfigure(0, weight=3)
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)
        self.home_frame.grid_rowconfigure(3, weight=1)
        self.home_frame.grid_rowconfigure(4, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(2, weight=1)

    def create_main_ui(self):
        self.home_frame = Frame(self.root)

        lab1 = Label(
            self.home_frame, text="Bookstore Management System", font=("Bahnschrift", 35)
        )
        lab1.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="we")

        btn1 = Button(
            self.home_frame,
            text="Manage Books",
            command=self.open_manage_books,
            width=35,
            pady=10,
            bg="gray",
            font=("Bahnschrift", 15),
        )
        btn1.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        btn2 = Button(
            self.home_frame,
            text="Manage Users",
            command=self.open_manage_users,
            width=35,
            pady=10,
            bg="gray",
            font=("Bahnschrift", 15),
        )
        btn2.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        btn3 = Button(
            self.home_frame,
            text="Manage Orders",
            command=self.open_manage_orders,
            width=35,
            pady=10,
            bg="gray",
            font=("Bahnschrift", 15),
        )
        btn3.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

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

    def show_home(self):
        if hasattr(self, "manage_books"):
            self.manage_books.hide()
        if hasattr(self, "manage_users"):
            self.manage_users.hide()
        if hasattr(self, "manage_orders"):
            self.manage_orders.hide()

        self.home_frame.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    app = BookstoreApp(root)
    root.mainloop()
