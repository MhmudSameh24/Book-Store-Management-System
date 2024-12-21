from tkinter import *
from Validation import Validation, MessageError
from Home_Window import BookstoreApp


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.validation = Validation()

        self.frame = Frame(root, padx=20, pady=20)
        self.frame.pack()

        Label(self.frame, text="Login", font=("Arial", 20)).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        Label(self.frame, text="Username:").grid(row=1, column=0, sticky=E)
        self.username_entry = Entry(self.frame)
        self.username_entry.grid(row=1, column=1)

        Label(self.frame, text="Password:").grid(row=2, column=0, sticky=E)
        self.password_entry = Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1)

        self.error_message = MessageError(
            self.frame, text="Invalid username or password"
        )
        self.error_message.hide()

        login_button = Button(self.frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.validation.check_username(
            username
        ) or not self.validation.check_password(password):
            self.error_message.show()
        else:
            self.error_message.hide()
            self.open_home_page()

    def open_home_page(self):
        self.frame.pack_forget()
        BookstoreApp(self.root)


if __name__ == "__main__":
    root = Tk()
    root.title("Login Page")
    root.geometry("300x200")

    login_page = LoginPage(root)

    root.mainloop()
