import psycopg2
import argparse

from psycopg2.errors import UniqueViolation
from psycopg2 import OperationalError

from models import User
from clcrypto import check_password, hash_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Username")
parser.add_argument("-p", "--password", help="Password")
parser.add_argument("-n", "--new_pass", help="New password")
parser.add_argument("-l", "--list", help="User list", action="store_true")
parser.add_argument("-d", "--delete", help="Delete user", action="store_true")
parser.add_argument("-e", "--edit", help="Edit user", action="store_true")
args = parser.parse_args()

def create_user(cursor, username, password):
    """
    Creates a new user in the database.
    :param cursor: Database cursor
    :param username: Username for the new user
    :param password: Plain-text password for the new user
    """
    if len(password) < 8:
        print("Password must be at least 8 characters long")
        return
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor)
            print("User created successfully")
        except UniqueViolation:
            print("User already exists")


def edit_user(cursor, username, password, new_pass):
    """
    Edits an existing user's password.
    :param cursor: Database cursor
    :param username: Username of the user to edit
    :param password: Current password for the user
    :param new_pass: New password to set for the user
    """
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User does not exist")
        return
    if not check_password(password, user.hashed_password):
        print("Wrong password")
        return
    if len(new_pass) < 8:
        print("New password must be at least 8 characters long")
        return

    user.hashed_password = hash_password(new_pass)
    user.save_to_db(cursor)
    print("Password updated successfully")


def delete_user(cursor, username, password):
    """
    Deletes an existing user after verifying password.
    :param cursor: Database cursor
    :param username: Username of the user to delete
    :param password: Password of the user for verification
    """
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User does not exist")
        return
    if not check_password(password, user.hashed_password):
        print("Wrong password")
        return
    user.delete(cursor)
    print("User deleted successfully")


def list_users(cursor):
    """
    Lists all the users in the database.
    :param cursor: Database cursor
    """
    users = User.load_all_users(cursor)
    if not users:
        print("No users found")
        return
    for user in users:
        print(user.username)

if __name__ == '__main__':
    """
    Main entry point of the script. Connects to the database and performs 
    user management commands based on provided command-line arguments.
    """
    try:
        cnx = psycopg2.connect(
            database="workshop2",
            user="postgres",
            password="coderslab",
            host="localhost",
        )

        cnx.autocommit = True
        cursor = cnx.cursor()

        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()

        cursor.close()
        cnx.close()

    except OperationalError:
        print("Database connection failed")
