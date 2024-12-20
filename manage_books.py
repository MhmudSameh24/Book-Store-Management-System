from book import Book
class ManageBooks:
    def add_book(self, book: Book):
        # Add a book to the Database
        pass
    def remove_book(self, book_id : int):
        # Remove a book from the Database
        pass
    def update_book(self, book: Book):
        # Update the book details
        pass
    def get_book(self, book_id : int) -> Book:
        # Get the book details
        pass
    def search_book(self, search_string: str) -> list[Book]:
        # Search for a book by title or author
        pass
    def get_all_books(self) -> list[Book]:
        # Get all the books
        pass
    def convert_data_to_book(self, row: dict) -> Book:
        # Convert the data to Book object
        pass
    def convert_rows(self, rows: list) -> list[Book]:
        # Convert the rows to Book objects
        pass


if __name__ == "__main__":
    objectOf = ManageBooks()