from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

# create database
CREATE_DB = "CREATE DATABASE workshop2;"

#create a table user
CREATE_USERS_TABLE = """ CREATE TABLE users(
id SERIAL PRIMARY KEY,
username VARCHAR(255) NOT NULL UNIQUE,
hashed_password VARCHAR(80) NOT NULL);"""

#create a table messages
CREATE_MESSAGES_TABLE = """ CREATE TABLE messages(
id SERIAL PRIMARY KEY,
from_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
to_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
text VARCHAR(255) NOT NULL,
creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"""

DB_USER = "postgres"
DB_PASSWORD = "coderslab"
DB_HOST = "localhost"

# create database
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

# create tables
try:
    cnx = connect(database="workshop2", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(CREATE_USERS_TABLE)
        print("Table 'users' created")
    except DuplicateTable:
        print("Table 'users' already exists")

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