
from database_utility import SQLite


main_database_path = "bookstore.db"
main_database_conection = SQLite(main_database_path)
main_database_conection.open()

# if __name__ == "__main__":
#     main_database_path = "Source/bookstore.db"
#     main_database_conection = SQLite(main_database_path)
#     main_database_conection.open()