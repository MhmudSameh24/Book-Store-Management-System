from tkinter import *
from tkinter import messagebox
import json
import os

COLOR_PRIMARY = "#2c3e50"
COLOR_BG = "#f8f9fa"
CONFIG_FILE = "config.json"

class SettingsWindow:
    def __init__(self, master, show_home):
        self.master = master
        self.show_home = show_home
        self.frame = Frame(master, bg=COLOR_BG)
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = Frame(self.frame, bg=COLOR_PRIMARY, height=60)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="Store Settings", font=("Segoe UI", 18, "bold"), 
              fg="white", bg=COLOR_PRIMARY).pack(side=LEFT, padx=20, pady=10)
        
        Button(header, text="Logout to Home", command=self.back_to_home, 
               bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), 
               bd=0, padx=15, cursor="hand2").pack(side=RIGHT, padx=20)

        # Settings Form
        form_frame = Frame(self.frame, bg="white", padx=40, pady=40, highlightbackground="#ddd", highlightthickness=1)
        form_frame.pack(expand=True)

        Label(form_frame, text="Store Name:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, sticky=W, pady=10)
        self.name_var = StringVar()
        Entry(form_frame, textvariable=self.name_var, font=("Segoe UI", 12), width=30).grid(row=0, column=1, pady=10, padx=10)

        Label(form_frame, text="Store Address:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, sticky=W, pady=10)
        self.address_var = StringVar()
        Entry(form_frame, textvariable=self.address_var, font=("Segoe UI", 12), width=30).grid(row=1, column=1, pady=10, padx=10)

        Label(form_frame, text="Contact Email:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, sticky=W, pady=10)
        self.email_var = StringVar()
        Entry(form_frame, textvariable=self.email_var, font=("Segoe UI", 12), width=30).grid(row=2, column=1, pady=10, padx=10)

        Button(form_frame, text="Save Settings", command=self.save_settings,
               bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"), width=15).grid(row=3, column=0, columnspan=2, pady=20)

    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.name_var.set(data.get("name", "My Bookstore"))
                    self.address_var.set(data.get("address", ""))
                    self.email_var.set(data.get("email", ""))
            except:
                pass

    def save_settings(self):
        data = {
            "name": self.name_var.get(),
            "address": self.address_var.get(),
            "email": self.email_var.get()
        }
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def display(self):
        self.frame.pack(fill=BOTH, expand=True)
        self.load_settings()

    def hide(self):
        self.frame.pack_forget()

    def back_to_home(self):
        self.hide()
        self.show_home()
