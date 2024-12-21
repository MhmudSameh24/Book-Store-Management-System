from tkinter import *
from Home_Window import BookstoreApp
from Validation import Validation, MessageError


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Login Page")
        self.validation = Validation()
        icon = PhotoImage(file="Icon.png")
        self.root.iconphoto(False, icon)
        self.frame = Frame(root, bd=2, relief="groove")
        self.frame.pack(padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=3)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(0, weight=2)
        self.frame.grid_columnconfigure(1, weight=1)

        lab1 = Label(self.frame, text="Login", font=("Arial", 50, "bold"))
        lab1.grid(row=0, column=0, columnspan=5, padx=10, pady=50, sticky="we")

        lab2 = Label(self.frame, text="Username:", font=("Arial", 15))
        lab2.grid(row=1, column=0, sticky="E", padx=10, pady=10)
        self.username_entry = Entry(self.frame, width=20, font=("Arial", 15))
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        lab3 = Label(self.frame, text="Password:", font=("Arial", 15))
        lab3.grid(row=2, column=0, sticky="E", padx=10, pady=10)
        self.password_entry = Entry(self.frame, show="●", width=20, font=("Arial", 15))
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        self.error_message = MessageError(
            self.frame, text="Invalid username or password", fg="red"
        )
        self.error_message.hide()

        login_button = Button(
            self.frame,
            text="Login",
            command=self.login,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            activebackground="#1FAF55",
            activeforeground="#252525",
            font=("Arial", 15, "bold"),
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if (
            not self.validation.check_username(username)
            or not self.validation.check_password(password)
            or not self.validation.check_admin(username, password)
        ):
            self.error_message.show()
        else:
            self.error_message.hide()
            self.open_home_page()

    def open_home_page(self):
        self.frame.pack_forget()
        BookstoreApp(self.root)


if __name__ == "__main__":
    root = Tk()
    login_page = LoginPage(root)

    root.mainloop()
