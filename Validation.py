from tkinter import *


class MessageError(Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid(row=4, column=0, columnspan=2, pady=5)
        self["fg"] = "red"
        self["font"] = ("Arial", 10, "bold")
        self.hide()

    def show(self):
        self.grid()

    def hide(self):
        self.grid_remove()


class Validation:
    Characters = "abcdefghijklmnopqrstuvwxyz"
    Numbers = "0123456789"
    

    correct_username = "admin"
    correct_password = "1234"
    
    admins = [(correct_username, correct_password)]

    def check_name(self, name):
        name = name.strip().lower()
        return all(let in Validation.Characters for let in name) and name != ""

    def check_number(self, number):
        number = number.strip()
        return all(let in Validation.Numbers for let in number) and number != ""

    def check_username(self, username):
        username = username.strip().lower()
        return (
            all(let in Validation.Characters + Validation.Numbers for let in username)
            and username != ""
        )

    def check_password(self, password):
        return password.strip() != ""
    
    def check_admin(self, username, password):
        for username_, password_ in Validation.admins:
            if username_ == username and password_ == password:
                return True;
        
        return False;

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Validation Example")
        self.geometry("400x200")

        self.validation = Validation()

        # Widgets
        Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.error_message = MessageError(self, text="Invalid username or password!")

        Button(self, text="Log In", command=self.validate_inputs).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def validate_inputs(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.validation.check_username(
            username
        ) or not self.validation.check_password(password):
            self.error_message.show()
        else:
            self.error_message.hide()
            print("Login Successful!")  # يمكن استدعاء الصفحة الرئيسية هنا


if __name__ == "__main__":
    app = App()
    app.mainloop()
