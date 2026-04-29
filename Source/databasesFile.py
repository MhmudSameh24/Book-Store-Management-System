import os
from database_utility import SQLite

base_dir = os.path.dirname(os.path.abspath(__file__))
main_database_path = os.path.join(base_dir, "bookstore.db")
main_database_conection = SQLite(main_database_path)
main_database_conection.open()

# if __name__ == "__main__":
#     main_database_path = "Source/bookstore.db"
#     main_database_conection = SQLite(main_database_path)
#     main_database_conection.open()