from tkinter import *
from tkinter import ttk, messagebox
from customtkinter import *
import re
import random

red = '#C00000'
dark_red = '#8B0000'
green = '#25D366'
dark_green = '#128C7E'
light_grey = '#D3D3D3'
white = '#E5E5E5'
black = '#252525'
class ManageUsers:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        self.frame = CTkFrame(master)
        self.create_ui()

    def create_ui(self):
        self.records = {}
        lab1 = CTkLabel(self.frame, text="Users Management", font=("Bahnschrift", 16))
        lab1.pack(pady=10)

        btn_home = CTkButton(
            self.frame, text="Back to Home", command=self.back_to_home, font=("Bahnschrift", 12)
        )
        btn_home.pack(pady=10)

        form_frame = CTkFrame(self.frame, fg_color="transparent")
        form_frame.pack(pady=10)

        CTkLabel(form_frame, text="Name", font=("Bahnschrift", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = CTkEntry(form_frame, width=200, font=("Bahnschrift", 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        CTkLabel(form_frame, text="Email", font=("Bahnschrift", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = CTkEntry(form_frame, width=200, font=("Bahnschrift", 12))
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        CTkButton(form_frame, text="Add User", command=self.add_user,  font=("Bahnschrift", 12)).grid(
            row=0, column=3, pady=10
        )

        CTkButton(form_frame, text="Update User", command=self.update_user, fg_color=green, text_color=black, hover_color=dark_green, font=("Bahnschrift", 12)).grid(
            row=1, column=3, pady=10
        )
        CTkButton(form_frame, text="Delete User", command=self.delete_user, fg_color=red, text_color=white, hover_color=dark_red, font=("Bahnschrift", 12)).grid(
            row=2, column=3, pady=10
        )

        self.search_txt = CTkEntry(form_frame, width=200, font=("Bahnschrift", 12))
        self.search_txt.grid(row=4, column=1, pady=10)
        CTkButton(form_frame, text="Search",command=self.search, font=("Bahnschrift", 12),width=18).grid(row=4, column=2, pady=10,padx=10)

        CTkButton(form_frame, text="Clear", command=self.clear_search,font=("Bahnschrift", 12),width=18).grid(row=4, column=3, pady=10)

        self.tree = ttk.Treeview(
            self.frame, columns=("id", "name", "email"), show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.load_records()
        self.show_records()
        self.tree.pack(pady=10)


    def validate_email(self, email):
        regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.search(regex, email):
            return True
        return False

    def validate_name(self, name):
        regex = "^[a-zA-Z ]+$"
        if re.search(regex, name):
            return True
        return False




    def add_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if name and email:
            if self.validate_name(name) == False or self.validate_email(email) == False:
                messagebox.showerror("Error", "Invalid name or email")
            else:
                messagebox.showinfo("Success", "User added successfully")
                record = (random.randint(1, 1000), name, email)
                self.add_record(record)
                self.add_to_view(record)
        else:
            messagebox.showerror("Error", "All fields are required")

    def delete_user(self):
        selected = self.tree.selection()
        if selected:
            id, name, email = self.tree.item(selected)["values"]
            self.delete_record((id, name, email))
            messagebox.showinfo("Success", "User deleted successfully")
            self.tree.delete(selected)
        else:
            messagebox.showerror("Error", "Please select a record to delete")
    
    def update_user(self):
        selected = self.tree.selection()
        if selected:
            if len(self.name_entry.get()) == 0 or len(self.email_entry.get()) == 0:
                messagebox.showerror("Error", "All fields are required")
            else:
                if self.validate_name(self.name_entry.get()) == False or self.validate_email(self.email_entry.get()) == False:
                    messagebox.showerror("Error", "Invalid name or email")
                else:
                    id, name, email = self.tree.item(selected)["values"]
                    self.update_record((id, name, email), (id, self.name_entry.get(), self.email_entry.get()))
                    name = self.name_entry.get()
                    email = self.email_entry.get()
                    messagebox.showinfo("Success", "User updated successfully")
                    self.tree.item(selected, values=(id, name, email))
        else:
            messagebox.showerror("Error", "Please select a record to update")
    

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()

 # --------------------------------- Database Operations ---------------------------------
    def add_record(self, record):
        # todo: add the record to the database
        self.records.add(record)
        pass

    def delete_record(self, record):
        # todo: delete the record from the database
        self.records.remove(record)
        pass

    def update_record(self,old_record, new_record):
        # todo: update the record in the database
        self.records.remove(old_record)
        self.records.add(new_record)        
        pass
# -----------------------------------------------------------------------------------------


    def is_matching(self, record, search_txt):
        # search with substring match in name and email (case insensitive)
        if search_txt.lower() in record[1].lower() or search_txt.lower() in record[2].lower():
            return True
        return False

    def search(self):
        search_txt = self.search_txt.get()
        new_records = []
        if search_txt:
            for record in self.tree.get_children():
                if self.is_matching(self.tree.item(record)["values"], search_txt):
                    new_records.append(self.tree.item(record)["values"])

            if new_records:
                self.tree.delete(*self.tree.get_children())
                for record in new_records:
                    self.tree.insert("", "end", values=record)
            else:
                messagebox.showinfo("Info", "No matching record found")
                self.clear_search()
        else:
            messagebox.showerror("Error", "Please enter a search text")
            self.show_records()

    def clear_search(self):
        self.search_txt.delete(0, END)
        self.show_records()

    # Todo : get the records from the database and display them in the treeview
    def add_to_view(self, record):
        self.tree.insert("", "end", values=record)
       
    
    def load_records(self):
        # some query to get the records
        self.records = {(1, "John Doe", ""), (2, "Jane Doe", ""), (3, "Alice", ""), (4, "Bob", ""), (5, "Charlie", "")}
        for record in self.records:
            self.add_record(record)

    def show_records(self):
        self.tree.delete(*self.tree.get_children())
        for record in self.records:
            self.add_to_view(record)

if __name__ == "__main__":
    root = CTk()
    root.title("Users Management")
    root.geometry("800x600")
    
    set_appearance_mode("light")
    ManageUsers(root, None).display()
    root.mainloop()
