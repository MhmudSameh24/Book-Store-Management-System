from tkinter import *
from tkinter import ttk, messagebox
from customtkinter import *
import re
from manage_users import ManageUsers as ManageUsersDB
from user import User

red = '#C00000'
dark_red = '#8B0000'
green = '#25D366'
dark_green = '#1FAF55'
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
        lab1 = CTkLabel(self.frame, text="Users Management", font=("Bahnschrift", 16))
        lab1.pack(pady=10)

        btn_home = CTkButton(
            self.frame, text="Back to Home", command=self.back_to_home, font=("Bahnschrift", 12)
        )
        btn_home.pack(pady=10)

        form_frame = CTkFrame(self.frame, fg_color="transparent")
        form_frame.pack(pady=10)

        CTkLabel(form_frame, text="Email", font=("Bahnschrift", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = CTkEntry(form_frame, width=200, font=("Bahnschrift", 12))
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        CTkButton(form_frame, text="Add User", command=self.add_user,  font=("Bahnschrift Bold", 12,)).grid(
            row=0, column=3, pady=10
        )

        CTkButton(form_frame, text="Update User", command=self.update_user, fg_color=green, text_color=black, hover_color=dark_green, font=("Bahnschrift Bold", 12)).grid(
            row=1, column=3, pady=10
        )
        CTkButton(form_frame, text="Delete User", command=self.delete_user, fg_color=red, text_color=white, hover_color=dark_red, font=("Bahnschrift Bold", 12)).grid(
            row=2, column=3, pady=10
        )
        CTkLabel(form_frame, text="Search Email", font=("Bahnschrift", 12)).grid(row=4, column=0, pady=10)
        self.search_txt = CTkEntry(form_frame, width=200, font=("Bahnschrift", 12))
        self.search_txt.grid(row=4, column=1, pady=10)
        CTkButton(form_frame, text="Search",command=self.search, font=("Bahnschrift", 12),width=18).grid(row=4, column=2, pady=10,padx=6)

        CTkButton(form_frame, text="Clear", command=self.clear_search,font=("Bahnschrift", 12),width=18).grid(row=4, column=3, padx=1)

        self.tree = ttk.Treeview(
            self.frame, columns=("id",  "email"), show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("email", text="Email")
        self.load_records()
        # self.show_records()
        self.tree.pack(pady=10)


    def validate_email(self, email):
        regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.search(regex, email):
            return True
        return False
 
    def add_user(self):
        email = self.email_entry.get()
        if len(email) and self.validate_email(email):
            state = self.add_record(email)
            if state:
                messagebox.showinfo("Success", "User added successfully")
                added_user = ManageUsersDB().get_user_by_email(email)
                self.add_to_view((added_user.get_id(), added_user.get_email()))
            else:
                messagebox.showerror("Error", "User already exists")
        else:
            messagebox.showerror("Error", "Please enter a valid email")
            

    def delete_user(self):
        selected = self.tree.selection()
        if selected:
            id = self.tree.item(selected)["values"][0]
            self.delete_record(int(id))
            self.tree.delete(selected)
            messagebox.showinfo("Success", "User deleted successfully")
        else:
            messagebox.showerror("Error", "User not found")
    
    def update_user(self):
        selected = self.tree.selection()
        if selected:
            new_email = self.email_entry.get()
            if len(new_email) and self.validate_email(new_email):
                updated_user = User()
                updated_user.set_id(self.tree.item(selected)["values"][0])
                updated_user.set_email(new_email)
                state = self.update_record(updated_user)
                if state:
                    self.tree.item(selected, values=(updated_user.get_id(), updated_user.get_email()))
                    messagebox.showinfo("Success", "User updated successfully")
                else:
                    messagebox.showerror("Error", "User already exists")
            else:
                messagebox.showerror("Error", "Please enter a valid email")
        else:
            messagebox.showerror("Error", "User not found")    

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()

 # --------------------------------- Database Operations ---------------------------------
    def add_record(self, new_email):
        # todo: add the record to the database
        state = ManageUsersDB().add_user(new_email)
        return state

    def delete_record(self, id):
        ManageUsersDB().remove_user(id)
    
    def update_record(self,updated_user):
        # todo: update the record in the database
        state = ManageUsersDB().update_user(updated_user)
        return state   
        pass
# -----------------------------------------------------------------------------------------

    def search(self):
        search_text = self.search_txt.get()
        if len(search_text):
            self.tree.delete(*self.tree.get_children())
            records = ManageUsersDB().search(search_text)
            for record in records:
                self.add_to_view((record.get_id(), record.get_email()))
        else:
            messagebox.showerror("Error", "Please enter a search text")        
          
    def clear_search(self):
        self.search_txt.delete(0, END)
        self.tree.delete(*self.tree.get_children())
        self.load_records()

    # Todo : get the records from the database and display them in the treeview
    def add_to_view(self, record):
        self.tree.insert("", "end", values=record)
       
    
    def load_records(self):
        records = ManageUsersDB().load_all_users()
        for record in records:
            self.add_to_view((record.get_id(), record.get_email()))
        
       

if __name__ == "__main__":
    root = CTk()
    root.title("Users Management")
    root.geometry("800x600")
    
    set_appearance_mode("light")
    ManageUsers(root, None).display()
    root.mainloop()
