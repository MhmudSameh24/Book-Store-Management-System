from tkinter import *

from PyQt5.sip import delete

from book import Book
from manage_books import *
from Validation import Validation
from tkinter import ttk, messagebox


class ManageOrders:
    def __init__(self, master, show_home):
        self.master = master
        self.orders = []
        self.manage_books = ManageBook(SQLite("bookstore.db"))
        self.show_home = show_home
        self.frame = Frame(master)
        self.orders = []
        self.create_ui()

    def create_ui(self):
        lab1 = Label(self.frame, text="Orders Management", font=("Arial", 16))
        lab1.pack(pady=10)

        btn_home = Button(
            self.frame, text="Back to Home", command=self.back_to_home, bg="gray"
        )
        btn_home.pack(pady=10)

        form_frame = Frame(self.frame)
        form_frame.pack(pady=10)

        lab2 = Label(form_frame, text="Buyer's Email").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.emial_entry = Entry(form_frame)
        self.emial_entry.grid(row=1, column=1, padx=5, pady=5)

        lab3 = Label(form_frame, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = Spinbox(
            form_frame,
            from_=1,
            to=100,
            increment=1,
            width=10,
        )
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        btn1 = Button(form_frame, text="Add To Cart", command=self.add_to_cart, bg="gray")
        btn1.grid(row=3, column=0, pady=10)

        btn2 = Button(
            form_frame, text="Remove To Cart", command=self.remove_from_cart, bg="gray"
        )
        btn2.grid(row=3, column=1, pady=10)

        btn3 = Button(form_frame, text="Clear cart", command=self.clear_cart, bg="gray")
        btn3.grid(row=3, column=2, pady=10)

        btn4 = Button(form_frame, text="Git Bill", command=self.add_order, bg="gray")
        btn4.grid(row=3, column=3, pady=10)

        # --------------------------------------------------
        # TODO: Implement output bill functionality

        # --------------------------------------

        # -------------------Books Table-------------------
        self.books_tree = ttk.Treeview(
            self.frame,
            columns=("book_id", "title", "author", "price"),
            show="headings",
        )
        self.books_tree.heading("book_id", text="Book ID")
        self.books_tree.heading("title", text="Title")
        self.books_tree.heading("author", text="Author")
        self.books_tree.heading("price", text="Price")
        self.books_tree.pack(pady=10)
        self.books_tree.pack(pady=10)
        self.load_books()

        # -------------------Orders Table-------------------
        self.tree = ttk.Treeview(
            self.frame,
            columns=("book_id", "title", "author", "price", "quantity"),
            show="headings",
        )

        self.tree.heading("book_id", text="Book ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("price", text="Price")
        self.tree.heading("quantity", text="Quantity")

        self.tree.pack(pady=10)
        self.load_orders()

    def add_to_cart(self):
        selected_item = self.books_tree.selection()
        if selected_item:
            item = self.books_tree.item(selected_item)
            book_id = item["values"][0]
            book = self.manage_books.get_book(book_id)
            quantity = int(self.quantity_entry.get())

            if quantity <= book.get_quantity():
                book.set_quantity(book.get_quantity() - quantity)
                self.manage_books.update_book(book)
                book.set_quantity(quantity)

                self.orders.append(book)

                self.load_books()
                self.load_orders()
            else:
                messagebox.showerror("Error", "the book is limited")
        else:
            messagebox.showerror("Error", "Select a book")

    def remove_from_cart(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            book_id = item["values"][0]
            book = self.manage_books.get_book(book_id)
            quantity = int(self.quantity_entry.get())

            for item in self.orders:
                if item.get_book_id() == book_id:
                    self.orders.remove(item)

            book.set_quantity(book.get_quantity() + quantity)
            self.manage_books.update_book(book)

            self.load_books()
            self.load_orders()
        else:
            messagebox.showerror("Error", "Select a book")

    def clear_cart(self):
        quantity = int(self.quantity_entry.get())

        for item in self.orders:
            book_id = item.get_book_id()
            book = self.manage_books.get_book(book_id)
            book.set_quantity(book.get_quantity() + item.get_quantity())
            self.manage_books.update_book(book)

        self.orders.clear()
        self.load_books()
        self.load_orders()

    def load_books(self):
        self.reset_book_table()
        self.books = self.manage_books.get_all_books()
        # print(self.books)
        for row in self.books:
            self.books_tree.insert("", END, values=(row.get_book_id(),
                                                    row.get_title(),
                                                    row.get_author(),
                                                    row.get_price(),
                                                    row.get_quantity()))

    def reset_book_table(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

    def load_orders(self):
        self.reset_order_table()
        for row in self.orders:
            self.tree.insert("", END, values=(row.get_book_id(),
                                                    row.get_title(),
                                                    row.get_author(),
                                                    row.get_price(),
                                                    row.get_quantity()))
        # self.books = self.manage_books.get_all_books()
        # # print(self.books)

        # for row in self.books:
        #     self.tree.insert("", END, values=(row.get_book_id(),
        #                                       row.get_title(),
        #                                       row.get_author(),
        #                                       row.get_price(),
        #                                       row.get_quantity()))

    def reset_order_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def add_order(self):
        book_id = self.book_id_entry.get()
        user_id = self.user_id_entry.get()
        quantity = self.quantity_entry.get()

        if book_id and user_id and quantity:
            self.orders.append((book_id, user_id, quantity))
            messagebox.showinfo("Success", "Order added successfully")
            self.load_orders()
        else:
            messagebox.showerror("Error", "All fields are required")

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.clear_cart()
        self.hide()
        self.show_home()
