from book import Book
from database_utility import SQLite


class ManageBook:
    def __init__(self, db: SQLite):
        self.db = db

    def add_book(self, book: Book):
        # Add a book to the Database
        self.db.free_execute(
            "INSERT INTO Books (title, author, price, quantity) VALUES (?, ?, ?, ?)",
            book.get_title(),
            book.get_author(),
            book.get_price(),
            book.get_quantity(),
        )
        self.db.commit()

    def remove_book(self, book_id: int):
        # Remove a book from the Database
        self.db.free_execute("DELETE FROM Books WHERE book_id = ?", book_id)
        self.db.commit()

    def update_book(self, book: Book):
        # Update the book details
        self.db.free_execute(
            "UPDATE Books SET title = ?, author = ?, price = ?, quantity = ? WHERE book_id = ?",
            book.get_title(),
            book.get_author(),
            book.get_price(),
            book.get_quantity(),
            book.get_book_id(),
        )
        self.db.commit()

    def get_book(self, book_id: int) -> Book:
        # Get the book details
        row = self.db.free_execute("SELECT * FROM Books WHERE book_id = ?", book_id)
        if len(row) == 0:
            return None
        return self.convert_data_to_book(row[0])

    def search_book(self, search_string: str) -> list[Book]:
        # Search for a book by title or author
        rows = self.db.free_execute(
            "SELECT * FROM Books WHERE title LIKE ? OR author LIKE ?",
            f"%{search_string}%",
            f"%{search_string}%"
        )
        return self.convert_rows(rows)

    def get_all_books(self) -> list[Book]:
        # Get all the books
        rows = self.db.free_execute("SELECT * FROM Books")
        return self.convert_rows(rows)

    def convert_data_to_book(self, row: dict) -> Book:
        # Convert the data to Book object
        book = Book()
        book.set_book_id(row["book_id"])
        book.set_title(row["title"])
        book.set_author(row["author"])
        book.set_price(row["price"])
        book.set_quantity(row["quantity"])
        return book

    def convert_rows(self, rows: list) -> list[Book]:
        # Convert the rows to Book objects
        books = []
        for row in rows:
            books.append(self.convert_data_to_book(row))
        return books


# test manage_books.py
if __name__ == "__main__":
    dbobj = SQLite("Source/bookstore.db")
    manage_books = ManageBook(dbobj)

    # Add a book
    book1 = Book()
    book1.set_title("Python Programming")
    book1.set_author("John Doe")
    book1.set_price(25.0)
    book1.set_quantity(100)
    manage_books.add_book(book1)
    print(book1)
    # Add another book
    book2 = Book()
    book2.set_title("Java Programming")
    book2.set_author("Jane Doe")
    book2.set_price(30.0)
    book2.set_quantity(50)
    manage_books.add_book(book2)
    print(book2)
    # Get all the books
    books = manage_books.get_all_books()
    for book in books:
        print(book)

    # # Search for a book
    search_books = manage_books.search_book("Python")
    for book in search_books:
        print(book)

    # # Update a book
    book1.set_price(30.0)
    book1.set_quantity(150)
    manage_books.update_book(book1)

    # # Get the updated book
    book = manage_books.get_book(1)
    print(book)
    print(book1)

    # # Remove a book
    manage_books.remove_book(2)

    # # Get all the books
    books = manage_books.get_all_books()
    for book in books:
        print(book)

    dbobj.open()
    dbobj.free_execute("DELETE FROM Books")
    dbobj.commit()
    dbobj.close()
