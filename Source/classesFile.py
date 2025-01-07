from manage_books import ManageBook
from manage_users import ManageUsers
from manage_bill import ManageBill
from databasesFile import main_database_conection



manage_book_conection = ManageBook(main_database_conection)
manage_user_conection = ManageUsers(main_database_conection)
manage_bill_conection = ManageBill(main_database_conection)



