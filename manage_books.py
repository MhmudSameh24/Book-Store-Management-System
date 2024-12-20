from book import Book
from database_utility import DataBase, DatabaseError, SQLite


class ManageBooks:
    def __init__(self, db: SQLite):
        self.db = db

    def add_book(self, book: Book):
        # Add a book to the Database
        self.db.free_execute(
            "INSERT INTO books (title, author, price, quantity) VALUES (?, ?, ?, ?)",
            (
                book.get_title(),
                book.get_author(),
                book.get_price(),
                book.get_quantity(),
            ),
        )

    def remove_book(self, book_id: int):
        # Remove a book from the Database
        self.db.free_execute("DELETE FROM books WHERE book_id = ?", (book_id,))

    def update_book(self, book: Book):
        # Update the book details
        self.db.free_execute(
            "UPDATE books SET title = ?, author = ?, price = ?, quantity = ? WHERE book_id = ?",
            (
                book.get_title(),
                book.get_author(),
                book.get_price(),
                book.get_quantity(),
                book.get_book_id(),
            ),
        )

    def get_book(self, book_id: int) -> Book:
        # Get the book details
        row = self.db.free_execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        return self.convert_data_to_book(row[0])

    def search_book(self, search_string: str) -> list[Book]:
        # Search for a book by title or author
        rows = self.db.free_execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            (f"%{search_string}%", f"%{search_string}%"),
        )
        return self.convert_rows(rows)

    def get_all_books(self) -> list[Book]:
        # Get all the books
        rows = self.db.free_execute("SELECT * FROM books")
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


if __name__ == "__main__":
    objectOf = ManageBooks()
