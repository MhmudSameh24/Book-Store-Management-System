from tkinter import *
from tkinter import ttk, messagebox


class ManageBooks:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master)
        self.create_ui()

    def create_ui(self):
        lab1 = Label(self.frame, text="Books Management", font=("Arial", 16))
        lab1.pack(pady=10)

        btn_home = Button(
            self.frame, text="Back to Home", command=self.show_home, bg="gray"
        )
        btn_home.pack(pady=10)

        form_frame = Frame(self.frame)
        form_frame.pack(pady=10)

        Label(form_frame, text="Title").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = Entry(form_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Author").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = Entry(form_frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Price").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = Entry(form_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(form_frame, text="Quantity").grid(row=3, column=0, padx=5, pady=5)
        self.quantity_entry = Entry(form_frame)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        Button(form_frame, text="Add Book", command=self.add_book, bg="gray").grid(
            row=4, column=0, pady=10
        )
        Button(
            form_frame, text="Update Book", command=self.update_book, bg="gray"
        ).grid(row=4, column=1, pady=10)

        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "title", "author", "price", "quantity"),
            show="headings",
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("price", text="Price")
        self.tree.heading("quantity", text="Quantity")
        self.tree.pack(pady=10)
        self.load_books()

    def load_books(self):
        sample_books = [
            (1, "Book A", "Author A", 15.5, 10),
            (2, "Book B", "Author B", 20.0, 5),
        ]
        for row in sample_books:
            self.tree.insert("", END, values=row)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if title and author and price and quantity:
            messagebox.showinfo("Success", "Book added successfully")
            self.load_books()
        else:
            messagebox.showerror("Error", "All fields are required")

    def update_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            book_id = item["values"][0]
            title = self.title_entry.get()
            author = self.author_entry.get()
            price = self.price_entry.get()
            quantity = self.quantity_entry.get()

            if title and author and price and quantity:
                messagebox.showinfo("Success", "Book updated successfully")
                self.load_books()
            else:
                messagebox.showerror("Error", "All fields are required")
        else:
            messagebox.showerror("Error", "Select a book to update")

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()
