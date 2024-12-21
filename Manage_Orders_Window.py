from tkinter import *
from tkinter import ttk, messagebox


class ManageOrders:
    def __init__(self, master, show_home):
        self.master = master
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

        Label(form_frame, text="Book ID").grid(row=0, column=0, padx=5, pady=5)
        self.book_id_entry = Entry(form_frame)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="User ID").grid(row=1, column=0, padx=5, pady=5)
        self.user_id_entry = Entry(form_frame)
        self.user_id_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = Entry(form_frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        Button(form_frame, text="Add Order", command=self.add_order, bg="gray").grid(
            row=3, column=0, pady=10
        )

        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "book_id", "user_id", "quantity"),
            show="headings",
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("book_id", text="Book ID")
        self.tree.heading("user_id", text="User ID")
        self.tree.heading("quantity", text="Quantity")
        self.tree.pack(pady=10)

        self.load_orders()

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, order in enumerate(self.orders):
            self.tree.insert("", "end", values=(idx + 1, *order))

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
        self.hide()
        self.show_home()
