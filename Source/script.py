# import sqlite3
# from faker import Faker
# import random

# # Initialize Faker instance for generating fake data
# fake = Faker()

# # Connect to the SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect('bookstore.db')
# cursor = conn.cursor()

# # Create the Books table (if it doesn't already exist)
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Books (
#     book_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     author TEXT NOT NULL,
#     price REAL NOT NULL,
#     quantity INTEGER NOT NULL
# )
# ''')

# # Function to generate random data and insert into Books table
# def insert_random_books(num_books):
#     for _ in range(num_books):
#         title = fake.sentence(nb_words=4)  # Generate a random book title
#         author = fake.name()               # Generate a random author name
#         price = round(random.uniform(5, 50), 2)  # Generate a random price between 5 and 50
#         quantity = random.randint(1, 100)  # Generate a random quantity between 1 and 100
        
#         cursor.execute('''
#         INSERT INTO Books (title, author, price, quantity)
#         VALUES (?, ?, ?, ?)
#         ''', (title, author, price, quantity))
    
#     conn.commit()
#     print(f"{num_books} books inserted into the Books table.")

# # Insert 100 random books into the table
# insert_random_books(100)

# # Close the database connection
# conn.close()


import sqlite3
from faker import Faker

# Initialize Faker instance for generating fake data
fake = Faker()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bookstore.db')
cursor = conn.cursor()

# Create the Users table (if it doesn't already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE
)
''')

# Function to generate random data and insert into Users table
def insert_random_users(num_users):
    for _ in range(num_users):
        email = fake.email()  # Generate a random email
        
        cursor.execute('''
        INSERT INTO Users (email)
        VALUES (?)
        ''', (email,))
    
    conn.commit()
    print(f"{num_users} users inserted into the Users table.")

# Insert 50 random users into the table
insert_random_users(5)

# Close the database connection
conn.close()
