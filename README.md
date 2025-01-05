# 📚 Bookstore Management System

This is a **Bookstore Management System** built using Python and SQLite. The system allows users to manage books, users, and orders through a graphical user interface (GUI) created with `tkinter`. It also includes functionality for generating bills and managing inventory.

## 👥 Contributors

- [Mahmoud Sameh](https://github.com/MhmudSameh24)
- [Mazen Ghanayem](https://github.com/Mazen-Ghanaym)
- [Youssef Gaber](https://github.com/Yousef-Gaber11)
- [Ahmed Wahba](https://github.com/abowahbaz)
- [Islam Imad](https://github.com/Islam-Imad)
- [Mohamed Mahmoud](https://github.com/mohammedmoud)

## ✨ Features

- **Manage Books**: Add, update, delete, and search for books in the database.
- **Manage Users**: Add, update, delete, and search for users.
- **Manage Orders**: Create and manage orders, generate bills, and track inventory.
- **Database Integration**: Uses SQLite for storing books, users, and orders.

## 📋 Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x**: The project is written in Python. You can download it from [python.org](https://www.python.org/downloads/).
- **SQLite**: The database used in this project. It comes pre-installed with Python.

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MhmudSameh24/Book-Store-Management-System.git
   cd Book-Store-Management-System/Source
   ```

2. **Install required packages**:
   The project uses the following Python packages:

   - `tkinter` (usually comes pre-installed with Python)
   - `sqlite3` (comes pre-installed with Python)
   - `faker` (for generating fake data, optional)

   To install the required packages, run:

   ```bash
   pip install faker
   ```

3. **Set up the database**:

   - Run the `schema.sql` script to create the necessary tables in the SQLite database:

     ```bash
     sqlite3 bookstore.db < schema.sql
     ```

   - Optionally, you can populate the database with fake data using the `script.py` file:

     ```bash
     python script.py
     ```

## 🚀 Running the Application

1. **Start the application**:
   Run the `Home_Window.py` file to start the application:

   ```bash
   python Home_Window.py
   ```

2. **Login**:

   - Use the following credentials to log in:
     - **Username**: `admin`
     - **Password**: `1234`

3. **Navigate the application**:
   - **Home Page**: From here, you can access the following sections:
     - **Manage Books**: Add, update, delete, and search for books.
     - **Manage Users**: Add, update, delete, and search for users.
     - **Manage Orders**: Create orders, generate bills, and manage inventory.

## 🗂️ Project Structure

- **`book.py`**: Contains the `Book` class for managing book data.
- **`database_utility.py`**: Handles database operations using SQLite.
- **`Home_Window.py`**: The main window of the application.
- **`Log_In_Window.py`**: The login window for the application.
- **`manage_bill.py`**: Manages bill generation and order processing.
- **`manage_books.py`**: Handles book-related operations.
- **`manage_users.py`**: Handles user-related operations.
- **`order.py`**: Manages orders and order-related operations.
- **`schema.sql`**: SQL script to create the database schema.
- **`script.py`**: Optional script to populate the database with fake data.
- **`user.py`**: Contains the `User` class for managing user data.
- **`Validation.py`**: Handles input validation and error messages.

## 🤝 Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## 🙏 Acknowledgments

- **Tkinter**: For providing the GUI framework.
- **SQLite**: For the lightweight database solution.
- **Faker**: For generating fake data for testing purposes.

---
