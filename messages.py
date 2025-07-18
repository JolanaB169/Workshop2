import psycopg2
import argparse

from models import *
from psycopg2 import OperationalError
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Username")
parser.add_argument("-p", "--password", help="Password")
parser.add_argument("-l", "--list", help="List all messages", action="store_true")
parser.add_argument("-t", "--to", help="Message recipient")
parser.add_argument("-s", "--send", help="Text message")
args = parser.parse_args()

def list_messages(cursor, username, password):
    """
    Authenticate user and list all messages sent to this user.
    :param cursor: Database cursor
    :param username: Username of the user whose messages will be listed
    :param password: User's password for authentication
    """
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User does not exist")
        return
    if not check_password(password, user.hashed_password):
        print("Password incorrect")
        return
    messages = Message.load_all_messages(cursor,user.id)
    if not messages:
        print("No messages found")
        return
    for message in messages:
        sender = User.load_user_by_id(cursor, message.from_id)
        print(f"From: {sender.username} Date: {message.creation_data} Message: {message.text}")


def send_message(cursor, from_username, password, to_username, message_text):
    """
    Authenticate sender and send a message to the recipient user.
    :param cursor: Database cursor
    :param from_username: Username of the sender
    :param password: Sender's password for authentication
    :param to_username: Username of the message recipient
    :param message_text: Text message
    """
    from_user = User.load_user_by_username(cursor, from_username)
    if not from_user:
        print("Sender user does not exist")
        return
    if not check_password(password, from_user.hashed_password):
        print("Password incorrect")
        return
    to_user = User.load_user_by_username(cursor, to_username)
    if not to_user:
        print("Recipient user does not exist")
        return
    if len(message_text) > 255:
        print("Message too long")
        return
    message = Message(from_id=from_user.id, to_id=to_user.id, text=message_text)
    message.save_to_db(cursor)
    print("Message sent successfully")


if __name__ == "__main__":
    """
    Main entry point: connects to the database, parses CLI arguments and 
    calls appropriate functions to list or send messages.
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

        if args.username and args.password and args.list:
            list_messages(cursor, args.username, args.password)
        elif args.username and args.password and args.to and args.send:
            send_message(cursor, args.username, args.password, args.to, args.send)
        else:
            parser.print_help()

        cursor.close()
        cnx.close()

    except OperationalError:
        print("Database connection failed")



