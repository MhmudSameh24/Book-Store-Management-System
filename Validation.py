from tkinter import *

def next(c):
    return chr(ord(c) + 1)

def prev(c):
    return chr(ord(c) - 1)

class MessageError:
    def __init__(self, parent, text = 'Something Wrong Here', color = 'red'):
        self.text = text
        self.frame = Frame(parent)
        self.label = Label(self.frame, text = text, fg = color);
        self.frame.pack()

    def hide(self):
        self.label.pack_forget()
        self.frame.config(height=0, width=0)
        self.label.config(text = "", height=0, width=0)

    def show(self):
        self.label.pack()
        self.label.config(text = self.text)

    def toggle(self):
        manager = self.label.winfo_manager()
        if manager == "pack":
            self.hide()
        else:
            self.show()

class Validation:
    Characters = "abcdefghijklmnopqrstuvwxyz"
    Numbers = "0123456789"

    def check_name(self, name):
        name = name.strip()
        name = name.lower()

        for let in name:
            if not let in Validation.Characters:
                return False

        return name != ""

    def check_number(self, number):
        number = number.strip()

        for let in number:
            if not let in Validation.Numbers:
                return False

        return number != ""

    def check_username(self, username):
        username = username.strip()
        username = username.lower()

        for let in username:
            if not let in Validation.Numbers and not let in Validation.Characters:
                return False

        return username != ""

    def check_password(self, password):
        password = password.strip()
        return password != ""

if __name__ == "__main__":
    valid = Validation()

    print(valid.check_name("moahdemd"))
    print(valid.check_number("1233"))
