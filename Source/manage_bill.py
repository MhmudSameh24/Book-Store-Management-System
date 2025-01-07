from functools import reduce
from book import Book
from database_utility import SQLite
from manage_books import ManageBook


class ManageBill:
    def __init__(self, db: SQLite):
        self.db = db
        self.manage_books = ManageBook(db)

    def __get_user_id(self, user_email: str) -> int:
        user_id = int(
            self.db.free_execute(
                "select user_id from users where email like ?", user_email
            )[0]["user_id"]
        )
        return user_id

    def __get_prices_of_some_books(self, books_ids: dict) -> dict:
        prices_data_row = self.db.free_execute(
            "select book_id, price from books where book_id in (?)", (books_ids.keys())
        )
        prices = dict()
        for row in prices_data_row:
            prices[int(row["book_id"])] = row["price"]

        return prices

    def __get_total_price_of_some_books(self, books_id: dict) -> float:
        prices = self.__get_prices_of_some_books(books_id)
        total_price = reduce(
            lambda x, y: x + y,
            [
                float(int(books_id[book_id]) * float(prices[book_id]))
                for book_id in prices.keys()
            ],
            0.0
        )
        return total_price

    def add_bill(self, books_id: dict, user_email: str) -> None:
        user_id = self.__get_user_id(user_email)
        prices = self.__get_prices_of_some_books(books_id)
        total_price = self.__get_total_price_of_some_books(books_id)

        self.db.free_execute(
            "insert into bills (user_id, total) values (?, ?)",
            user_id,
            total_price,
        )

        last_bill_id = self.db.free_execute("select bill_id from bills limit 1")[0][
            "bill_id"
        ]

        for book_id in books_id.keys():
            self.db.free_execute(
                "insert into bookorder (book_id, price_per_book, quatity, bill_id) values (?, ?, ?, ?)",
                user_id,
                prices[book_id],
                books_id[book_id],
                last_bill_id,
            )

        self.db.commit()

    def create_bill(self, books_ids: dict) -> str:
        bill: str = ""
        self.db.open()
        print("create_bill: ")
        print(books_ids)
        print(list(books_ids.keys()))
        placeholder = f"select * from Books where book_id in ({', '.join(['?']*len(books_ids.keys()))})"
        books_data_rows = self.manage_books.convert_rows(
            self.db.free_execute_bill_manage(
                placeholder, *books_ids.keys()
            )
        )
        total_price: float = 0.0
        print(books_data_rows)
        for book in books_data_rows:
            sub_bill: str = ""
            sub_bill += f"book title : {book.get_title()}\n"
            sub_bill += f"quantity : {books_ids[book.get_book_id()]}\n"
            sub_bill += f"book price : {book.get_price() * books_ids[book.get_book_id()]: .2f}\n"

            bill += sub_bill
            bill += str(str("-") * 15) + "\n"

            total_price += book.get_price() * books_ids[book.get_book_id()]

        bill += f"total price : {total_price : .2f}\n"

        
        return bill

    def get_user_history(self, user_id: int) -> list[str]:
        pass


if __name__ == "__main__":
    db = SQLite("bookstore.db")
    object_of_manage_bill = ManageBill(db)
