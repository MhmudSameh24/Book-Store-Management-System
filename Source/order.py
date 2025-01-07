from book import Book
from database_utility import SQLite
from manage_books import ManageBook
from manage_bill import ManageBill


class Order:
    def __init__(self, db: SQLite):
        # {book_id : quantity}
        self.books = dict() 
        self.db = db
        self.manage_books = ManageBook(self.db)
        self.manage_bill = ManageBill(self.db)
    
    def add_book(self, book_id : int, quantity : int = 1 ) -> None:
        if book_id not in self.books:
            self.books[book_id] = quantity
            is_there_enough_quantity = self.verify_quantity(book_id)
            if not is_there_enough_quantity:
                self.books.pop(book_id)
        else:
            self.books[book_id] += quantity
            is_there_enough_quantity = self.verify_quantity(book_id)
            if not is_there_enough_quantity:
                self.books[book_id] -= quantity
    
    def remove_book(self, book_id : int, quantity : int  = 1) -> None:
        if book_id in self.books and self.books[book_id] - quantity >= 0:
            self.books[book_id] -= quantity
        if book_id in self.books and self.books[book_id] <= 0:
            self.books.pop(book_id)

    def get_ordered_books(self) -> list[Book]:
        placeholder = f"select * from Books where book_id in ({', '.join(['?']*len(self.books.keys()))})"
        books_data = self.db.free_execute_bill_manage(
            placeholder,
            *self.books.keys()
        )
        ordered_books = [self.manage_books.convert_data_to_book(row) for row in books_data]
        return ordered_books

    def verify_quantity(self, book_id : int) -> bool:
        if book_id not in self.books:
            return False
        
        data_row = self.db.free_execute(
            "select quantity from books where book_id = ?",
            book_id
        )

        if len(data_row) == 0:
            return False
        real_quantity = int(data_row[0]["quantity"])
        return (real_quantity >= self.books[book_id])
    
    def create_bill(self):
        return self.manage_bill.create_bill(self.books)

    def complete_purchase(self, user_email : str) -> bool:
        for book_id in self.books.keys():
            isgood = self.verify_quantity(book_id)
            if not isgood:
                return False
        
        for book_id in self.books.keys():
            newBook = self.manage_books.get_book(book_id)
            newBook.set_quantity(newBook.get_quantity() - self.books[book_id])
            self.manage_books.update_book(newBook)
        
        # self.manage_bill.add_bill(self.books, user_email)
        self.books.clear()
        
        return True


if __name__ == "__main__":
    db = SQLite("bookstore.db")
    object_of_order = Order(db)