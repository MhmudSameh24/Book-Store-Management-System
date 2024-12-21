from tkinter import *
from tkinter import ttk, messagebox


class ManageUsers:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master)
        self.create_ui()

    def create_ui(self):
        lab1 = Label(self.frame, text="Users Management", font=("Arial", 16))
        lab1.pack(pady=10)

        btn_home = Button(
            self.frame, text="Back to Home", command=self.back_to_home, bg="gray"
        )
        btn_home.pack(pady=10)

        form_frame = Frame(self.frame)
        form_frame.pack(pady=10)

        Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = Entry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        Button(form_frame, text="Add User", command=self.add_user, bg="gray").grid(
            row=2, column=0, pady=10
        )

        self.tree = ttk.Treeview(
            self.frame, columns=("id", "name", "email"), show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.pack(pady=10)

    def add_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if name and email:
            messagebox.showinfo("Success", "User added successfully")
        else:
            messagebox.showerror("Error", "All fields are required")

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()  # إخفاء الإطار الحالي
        self.show_home()
