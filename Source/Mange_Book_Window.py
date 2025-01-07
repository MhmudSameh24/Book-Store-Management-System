from tkinter import *
from book import Book
from manage_books import *
from Validation import Validation
from tkinter import ttk, messagebox

# from databasesFile import main_database_conection
from classesFile import manage_book_conection

red = "#C00000"
dark_red = "#8B0000"
green = "#25D366"
blue = "#128C7E"
dark_blue = "#075E54"
light_grey = "#D3D3D3"
color_txt = "#252525"
color_frame = "#E5E5E5"
yellow = "#ffe400"


class ManageBooks:
    def __init__(self, master, show_home):
        # self.dbobj = SQLite("bookstore.db")
        # self.manage_books = ManageBook(SQLite("Source/bookstore.db"))
        self.manage_books = manage_book_conection
        self.valid = Validation()
        self.books = []
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master)
        self.create_ui()

    def create_ui(self):
        # ***************************** books data entry (add book, update book, delete book) ***************************
        books_data = Frame(self.frame, bg=color_frame)
        books_data.grid(row=0, column=0, rowspan=2, padx=50, sticky="nesw")

        # Title 1
        title_frame = Frame(books_data, bg=color_frame)
        title_frame.grid(row=0, column=0, sticky="nesw", pady=20, padx=20)

        lab1 = Label(
            books_data,
            text="Books Management",
            fg=color_txt,
            font=("Arial", 20),
            bg=color_frame,
        )
        lab1.grid(pady=10, row=0, column=0, sticky="nesw")
        # -------------------------------------------------------------------

        # Input Books 2
        form_frame = Frame(books_data, bg=color_frame)
        form_frame.grid(row=1, column=0)

        Label(
            form_frame, text="Title", font=("Arial", 10), bg=color_frame, fg=color_txt
        ).grid(row=0, column=0, padx=5, pady=5, sticky="nesw")
        self.title_entry = Entry(form_frame, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        Label(
            form_frame, text="Author", font=("Arial", 10), bg=color_frame, fg=color_txt
        ).grid(row=1, column=0, padx=5, pady=5, sticky="nesw")
        self.author_entry = Entry(form_frame, font=("Arial", 10))
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nesw")

        Label(
            form_frame, text="Price", font=("Arial", 10), bg=color_frame, fg=color_txt
        ).grid(row=2, column=0, padx=5, pady=5, sticky="nesw")
        self.price_entry = Entry(form_frame, font=("Arial", 10))
        self.price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nesw")

        Label(
            form_frame,
            text="Quantity",
            font=("Arial", 10),
            bg=color_frame,
            fg=color_txt,
        ).grid(row=3, column=0, padx=5, pady=5, sticky="nesw")
        self.quantity_entry = Entry(form_frame, font=("Arial", 10))
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nesw")
        # -------------------------------------------------------------------

        # Button books 3
        buttons_frame = Frame(books_data, bg=color_frame)
        buttons_frame.grid(row=2, column=0, pady=10, sticky="nesw")
        Button(
            buttons_frame,
            text="Add Book",
            command=self.add_book,
            bg=blue,
            fg="#ffffff",
            width=self.quantity_entry["width"] * 2,
            activebackground=dark_blue,
            activeforeground="#000000",
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="nesw")

        Button(
            buttons_frame,
            text="Update Book",
            command=self.update_book,
            bg=blue,
            fg="#ffffff",
            width=self.quantity_entry["width"] * 2,
            activebackground=dark_blue,
            activeforeground="#000000",
        ).grid(row=1, column=0, columnspan=2, pady=10, sticky="nesw")

        Button(
            buttons_frame,
            text="Delete Book",
            command=self.delete_book,
            bg=red,
            fg="#ffffff",
            activebackground=dark_red,
            activeforeground="#000000",
            width=self.quantity_entry["width"] * 2,
        ).grid(row=2, column=0, columnspan=2, pady=10, sticky="nesw")
        # -------------------------------------------------------------------

        # Goto Home Button 3
        # home_frame = Frame(books_data, bg = color_frame)
        # home_frame.grid(row = 3, column = 0, sticky="nesw")

        btn_home = Button(
            buttons_frame,
            text="Back to Home",
            command=self.show_home,
            bg=color_txt,
            fg="#ffffff",
            width=self.quantity_entry["width"] * 2,
            activebackground=light_grey,
            activeforeground="#000000",
        )
        btn_home.grid(pady=50, row=3, column=0, columnspan=2, sticky=S)
        # -------------------------------------------------------------------
        # ***************************************************************************************************************

        # ********************************************* search book *******************************************
        search_frame = Frame(self.frame, bg=color_frame)
        search_frame.grid(row=0, column=1, sticky="WE")

        label_search = Label(
            search_frame,
            text="Search",
            width=20,
            font=("Arial", 16),
            bg=color_frame,
            fg=color_txt,
        )
        label_search.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

        self.search_entry = Entry(search_frame, width=40, font=("Arial", 13))
        self.search_entry.grid(row=1, column=2, padx=10, pady=10, sticky="WE")

        btn_search = Button(
            search_frame,
            text="Search For Book",
            command=self.search_book,
            width=self.quantity_entry["width"] + 10,
            bg=blue,
            fg="#ffffff",
            activebackground=dark_blue,
            activeforeground="#000000",
        )
        btn_search.grid(row=1, column=3, padx=10, pady=10, sticky="WE")

        btn_clear_results = Button(
            search_frame,
            text="Delete Results",
            command=self.delete_results,
            width=self.quantity_entry["width"] + 10,
            bg=red,
            fg="#ffffff",
            activebackground=dark_red,
            activeforeground="#000000",
        )
        btn_clear_results.grid(row=1, column=4, padx=10, pady=10, sticky="WE")
        # **********************************************************************************************

        # ********************************************* table books *******************************************

        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "title", "author", "price", "quantity"),
            show="headings",
            height=20,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("price", text="Price")
        self.tree.heading("quantity", text="Quantity")
        self.tree.grid(row=1, column=1)
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)

        self.load_books()

    def load_books(self):
        # self.books = [
        #     (1, "Book A", "Author A", 15.5, 10),
        #     (2, "Book B", "Author B", 20.0, 5),
        # ]
        self.reset_table()

        self.books = self.manage_books.get_all_books()
        # print(self.books)

        for row in self.books:
            self.tree.insert(
                "",
                END,
                values=(
                    row.get_book_id(),
                    row.get_title(),
                    row.get_author(),
                    row.get_price(),
                    row.get_quantity(),
                ),
            )

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

        if title and author and price and self.valid.check_number(quantity):
            self.manage_books.add_book(book)
            self.load_books()
            self.reset_form()
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

            if title and author and price and self.valid.check_number(quantity):
                book = self.manage_books.get_book(book_id)
                book.set_title(title)
                book.set_author(author)
                book.set_price(price)
                book.set_quantity(quantity)

                self.manage_books.update_book(book)
                self.load_books()
                self.reset_form()
                messagebox.showinfo("Success", "Book updated successfully")
            else:
                messagebox.showerror("Error", "All fields are required")
        else:
            messagebox.showerror("Error", "Select a book to update")

    def delete_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.reset_form()
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
                self.tree.insert(
                    "",
                    END,
                    values=(
                        row.get_book_id(),
                        row.get_title(),
                        row.get_author(),
                        row.get_price(),
                        row.get_quantity(),
                    ),
                )

    def delete_results(self):
        self.load_books()

    def reset_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def reset_form(self):
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.quantity_entry.delete(0, END)

    def on_item_click(self, event):

        # Get the selected item
        selected_item = self.tree.selection()  # Get the focused item
        if selected_item:
            self.reset_form()
            item_data = self.tree.item(selected_item)
            print(item_data["values"])
            self.title_entry.insert(0, item_data["values"][1])
            self.author_entry.insert(0, item_data["values"][2])
            self.price_entry.insert(0, item_data["values"][3])
            self.quantity_entry.insert(0, item_data["values"][4])

            print("Item Data:", item_data)  # Print the data
            print("Values:", item_data["values"])  # Print the values (columns)

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()
