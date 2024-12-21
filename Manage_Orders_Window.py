from tkinter import *


from book import Book
from manage_books import *
from Validation import Validation
from tkinter import ttk, messagebox

red = '#C00000'
dark_red = '#8B0000'
green = '#25D366'
dark_green = '#128C7E'
light_grey = '#D3D3D3'
white = '#252525'
black = '#E5E5E5'
yellow = "#ffe400"

class ManageBooks:
    def __init__(self, master, show_home):
        # self.dbobj = SQLite("bookstore.db")
        self.manage_books = ManageBook(SQLite("bookstore.db"))
        self.valid = Validation()
        self.books = []
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master, bg = black)
        self.master["bg"] = black
        self.create_ui()


    def create_ui(self):
        #***************************** books data entry (add book, update book, delete book) ***************************
        books_data = Frame(self.frame, bg = black)
        books_data.grid(row = 0, column = 0, rowspan = 2, padx = 50, sticky="nesw")

        # Title 1
        title_frame = Frame(books_data, bg = black)
        title_frame.grid(row = 0, column = 0, sticky="nesw", pady = 20, padx = 20)

        lab1 = Label(books_data, text="Books Management", fg = white, font=("Arial", 20), bg = black)
        lab1.grid(pady=10, row = 0, column = 0, sticky="nesw")
        # -------------------------------------------------------------------

        # Input Books 2
        form_frame = Frame(books_data, bg = black)
        form_frame.grid(row = 1, column = 0)

        Label(form_frame, text="Title",  font=("Arial", 10), bg = black, fg = white).grid(row=0, column=0, padx = 5, pady=5, sticky='nesw')
        self.title_entry = Entry(form_frame,  font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, padx = 5, pady=5, sticky="nesw")

        Label(form_frame, text="Author",  font=("Arial", 10), bg = black, fg = white).grid(row=1, column=0, padx = 5, pady=5, sticky='nesw')
        self.author_entry = Entry(form_frame,  font=("Arial", 10))
        self.author_entry.grid(row=1, column=1, padx = 5,pady=5, sticky="nesw")

        Label(form_frame, text="Price",  font=("Arial", 10), bg = black, fg = white).grid(row=2, column=0, padx = 5, pady=5, sticky='nesw')
        self.price_entry = Entry(form_frame,  font=("Arial", 10))
        self.price_entry.grid(row=2, column=1, padx = 5, pady=5, sticky="nesw")

        Label(form_frame, text="Quantity",  font=("Arial", 10), bg = black, fg = white).grid(row=3, column=0, padx = 5, pady=5, sticky='nesw')
        self.quantity_entry = Entry(form_frame,  font=("Arial", 10))
        self.quantity_entry.grid(row=3, column=1, padx = 5, pady=5, sticky="nesw")
        # -------------------------------------------------------------------


        # Button books 3
        buttons_frame = Frame(books_data, bg = black)
        buttons_frame.grid(row = 2, column = 0, pady=10, sticky="nesw")
        Button (
            buttons_frame, text="Add Book", command=self.add_book, bg=dark_green, fg = white, width = self.quantity_entry["width"] * 2
        ).grid(row=0, column=0, columnspan = 2, pady=10, sticky="nesw")

        Button(
            buttons_frame, text="Update Book", command=self.update_book, bg=dark_green, fg = white, width = self.quantity_entry["width"] * 2
        ).grid(row=1, column=0, columnspan = 2, pady=10, sticky="nesw")

        Button(
            buttons_frame, text="Delete Book", command=self.delete_book, bg=dark_red, fg = white, width = self.quantity_entry["width"] * 2
        ).grid(row=2, column=0, columnspan = 2, pady=10, sticky="nesw")
        # -------------------------------------------------------------------

        # Goto Home Button 3
        # home_frame = Frame(books_data, bg = black)
        # home_frame.grid(row = 3, column = 0, sticky="nesw")

        btn_home = Button(
            buttons_frame, text="Back to Home", command=self.show_home, bg=white, fg = black, width = self.quantity_entry["width"] * 2
        )
        btn_home.grid(pady=10, row = 3, column = 0, columnspan = 2, sticky="nesw")
        # -------------------------------------------------------------------
        #***************************************************************************************************************



        #********************************************* search book *******************************************
        search_frame = Frame(self.frame, bg = black)
        search_frame.grid(row = 0, column = 1, sticky = 'WE')

        label_search = Label(search_frame, text = "Search", width = 20, font=("Arial", 16), bg = black, fg = white)
        label_search.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky="WE")

        self.search_entry = Entry(search_frame, width = 40, font=("Arial", 13))
        self.search_entry.grid(row = 1, column = 2, padx = 10, pady = 10, sticky="WE")

        btn_search = Button(search_frame, text = "Search For Book", command=self.search_book, width = self.quantity_entry["width"] * 2, bg=dark_green, fg = white)
        btn_search.grid(row = 1, column = 3, padx = 10, pady = 10, sticky="WE")

        btn_clear_results = Button(search_frame, text = "Delete Results", command=self.delete_results, width = self.quantity_entry["width"] * 2, bg=white, fg = black)
        btn_clear_results.grid(row = 1, column = 4, padx = 10, pady = 10, sticky="WE")
        #**********************************************************************************************


        #********************************************* table books *******************************************

        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "title", "author", "price", "quantity"),
            show="headings",
            height = 20
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("price", text="Price")
        self.tree.heading("quantity", text="Quantity")
        self.tree.grid(row = 1, column = 1)
        self.load_books()


    def load_books(self):
        # self.books = [
        #     (1, "Book A", "Author A", 15.5, 10),
        #     (2, "Book B", "Author B", 20.0, 5),
        # ]
        self.reset_table()

        self.books = self.manage_books.get_all_books()
        print(self.books)

        for row in self.books:
            self.tree.insert("", END, values=(row.get_book_id(),
                                              row.get_title(),
                                              row.get_author(),
                                              row.get_price(),
                                              row.get_quantity()))

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        book = Book()
        book.set_title(title)
        book.set_author(author)
        book.set_price(price)
        book.set_quantity(quantity)

        if title and author and self.valid.check_number(price) and self.valid.check_number(quantity):
            self.manage_books.add_book(book)
            self.load_books()
            messagebox.showinfo("Success", "Book added successfully")
        else:
            if title and author and price and quantity:
                messagebox.showerror("Error", "Price or quantity should be number")
            else:
                messagebox.showerror("Error", "All fields are required")

    def update_book(self):
        selected_item = self.tree.selection()
        print(selected_item)
        if selected_item:
            item = self.tree.item(selected_item)
            print(item)
            book_id = item["values"][0]
            print(book_id)
            title = self.title_entry.get()
            author = self.author_entry.get()
            price = self.price_entry.get()
            quantity = self.quantity_entry.get()

            if title and author and self.valid.check_number(price) and self.valid.check_number(quantity):
                book = self.manage_books.get_book(book_id)
                book.set_title(title)
                book.set_author(author)
                book.set_price(price)
                book.set_quantity(quantity)

                self.manage_books.update_book(book)
                self.load_books()
                messagebox.showinfo("Success", "Book updated successfully")
            else:
                messagebox.showerror("Error", "All fields are required")
        else:
            messagebox.showerror("Error", "Select a book to update")

    def delete_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            book_id = item["values"][0]
            self.manage_books.remove_book(book_id)
            self.load_books()
            messagebox.showinfo("Success", "Book Deleted successfully")
        else:
            messagebox.showerror("Error", "Select a book to Delete")

    def search_book(self):
        search = self.search_entry.get()
        if search:
            self.reset_table()

            self.books = self.manage_books.search_book(search)
            print(self.books)

            for row in self.books:
                self.tree.insert("", END, values=(row.get_book_id(),
                                                  row.get_title(),
                                                  row.get_author(),
                                                  row.get_price(),
                                                  row.get_quantity()))
        # else:


    def delete_results(self):
        self.load_books()

    def reset_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def display(self):
        self.frame.pack(pady = 50, padx = 50, fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()
