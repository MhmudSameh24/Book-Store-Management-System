from tkinter import *
from tkinter import ttk, messagebox
import random


class ManageUsers:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master)
        self.create_ui()
 

    def create_ui(self):
        self.records = {}
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

        Button(form_frame, text="Delete User", command=self.delete_record, bg="gray").grid(
            row=2, column=1, pady=10
        )

        Button(form_frame, text="Update User", command=self.update_record, bg="gray").grid(
            row=2, column=2, pady=10
        )
        
    
        self.search_txt = Entry(form_frame)
        self.search_txt.grid(row=3, column=1, pady=10)
        Button(form_frame, text="Search", bg="gray",command=self.search).grid(row=3, column=2, pady=10)


        self.tree = ttk.Treeview(
            self.frame, columns=("id", "name", "email"), show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.load_records()
        self.show_records()
        self.tree.pack(pady=10)
     

    def add_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if name and email:
            messagebox.showinfo("Success", "User added successfully")
            record = (random.randint(1, 1000), name, email)
            self.add_record(record)
        else:
            messagebox.showerror("Error", "All fields are required")

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()
    
    def add_record(self,record):
        # todo: add the record to the database
        self.records.add(record)
        self.tree.insert("", "end", values=record)

    def delete_record(self):
        # todo: delete the record from the database
        selected = self.tree.selection()
        if selected:
            id,name,email = self.tree.item(selected)["values"]
            self.records.remove((id,name,email))
            messagebox.showinfo("Success", "User deleted successfully")
            self.tree.delete(selected)
        else:
            messagebox.showerror("Error", "Please select a record to delete")

    def update_record(self):
        # todo: update the record in the database
        selected = self.tree.selection()
        if selected:
            if len(self.name_entry.get()) == 0 or len(self.email_entry.get()) == 0:
                messagebox.showerror("Error", "All fields are required")
            else:
                id,name,email = self.tree.item(selected)["values"]
                self.records.remove((id,name,email))
                name = self.name_entry.get()
                email = self.email_entry.get()
                self.records.add((id,name,email))
                messagebox.showinfo("Success", "User updated successfully")
                self.tree.item(selected, values=(id, name, email))
                
        else:
            messagebox.showerror("Error", "Please select a record to update")
        


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
        else:
            messagebox.showerror("Error", "Please enter a search text")
            self.show_records()
        
        

    # Todo : get the records from the database and display them in the treeview
    def load_records(self):
    # some query to get the records
        self.records = {(1, "John Doe", ""), (2, "Jane Doe", ""), (3, "Alice", ""), (4, "Bob", ""), (5, "Charlie", "")}
        for record in self.records:
            self.add_record(record)

    def show_records(self):
        self.tree.delete(*self.tree.get_children())
        for record in self.records:
            self.add_record(record)

if __name__ == "__main__":
    root = Tk()
    root.title("Users Management")
    root.geometry("600x400")
    ManageUsers(root, None).display()
    root.mainloop()