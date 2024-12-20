class Book:
    def __init__(self):
        self.book_id = 0
        self.title = ""
        self.author = ""
        self.price = 0.0
        self.quantity = 0

    def set_book_id(self, book_id : int):
        self.book_id = book_id

    def get_book_id(self) -> int:
        return self.book_id

    def set_title(self, title : str):
        self.title = title

    def get_title(self) -> str:
        return self.title

    def set_author(self, author : str):
        self.author = author

    def get_author(self) -> str:
        return self.author

    def set_price(self, price : float):
        self.price = price

    def get_price(self) -> float:
        return self.price

    def set_quantity(self, quantity : int):
        self.quantity = quantity

    def get_quantity(self) -> int:
        return self.quantity

    def __str__(self):
        return f"Book ID: {self.book_id},\
            Title: {self.title},\
            Author: {self.author},\
            Price: {self.price},\
            Quantity: {self.quantity}"

    def __repr__(self):
        return f"Book ID: {self.book_id},\
            Title: {self.title},\
                Author: {self.author},\
                    Price: {self.price},\
                        Quantity: {self.quantity}"



if __name__ == "__main__":
    objectOf = Book()