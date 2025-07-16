from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

# SQL statement to create a new database
CREATE_DB = "CREATE DATABASE workshop2;"

# SQL statement to  create the 'users' table
CREATE_USERS_TABLE = """ CREATE TABLE users(
id SERIAL PRIMARY KEY,
username VARCHAR(255) NOT NULL UNIQUE,
hashed_password VARCHAR(80) NOT NULL);"""

# SQL statement to create the 'messages' table
CREATE_MESSAGES_TABLE = """ CREATE TABLE messages(
id SERIAL PRIMARY KEY,
from_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
to_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
text VARCHAR(255) NOT NULL,
creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"""

# Database connection credentials
DB_USER = "postgres"
DB_PASSWORD = "coderslab"
DB_HOST = "localhost"

# === Step 1: Create the database ===
try:
    cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(CREATE_DB)
        print("Database created")
    except DuplicateDatabase:
        print("Database already exists")
    cursor.close()
    cnx.close()
except OperationalError as e:
    print(f"Connection error: {e}")
    exit(1)

# === Step 2: Create tables in the new database ===
try:
    # Connect to the newly created database
    cnx = connect(database="workshop2", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()

    # Try to create the 'users' table
    try:
        cursor.execute(CREATE_USERS_TABLE)
        print("Table 'users' created")
    except DuplicateTable:
        print("Table 'users' already exists")

    # Try to create the 'messages' table
    try:
        cursor.execute(CREATE_MESSAGES_TABLE)
        print("Table 'messages' created")
    except DuplicateTable:
        print("Table 'messages' already exists")

    cursor.close()
    cnx.close()
except OperationalError as e:
    print(f"Connection error: {e}")
    exit(1)