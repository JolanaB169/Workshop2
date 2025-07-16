from clcrypto import hash_password
from datetime import datetime, timedelta

# class User
class User:
    """
    Class representing a user from the 'users' table in the database.
    """
    def __init__(self, username="", password="", salt=""):
        """
        Initializes a new User object.
        :param username: The username of the user.
        :param password: The password of the user. Will be hashed.
        :param salt: Optional salt for hashing. If empty, it will be generated.
        """
        self._id = -1 # -1 means object is not yet saved in DB
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        """
        Returns the ID of the user.
        """
        return self._id

    @property
    def hashed_password(self):
        """
        Returns the hashed password (read-only).
        """
        return self._hashed_password

    def set_password(self, password, salt=""):
        """
        Hashes and sets a new password for the user.
        :param password: The new plain-text password.
        :param salt: Optional salt.
        """
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        """
        Automatically sets the hashed password for the user.
        """
        self.set_password(password)

    def save_to_db(self, cursor):
        """
        Saves the user to the database.
        If the user is new (id == -1), inserts a new row.
        If the user already exists, it will be updated.
        """
        if self._id == -1:
            sql = """
                  INSERT INTO users (username, hashed_password) 
                  VALUES (%s, %s) RETURNING id;
                  """
            cursor.execute(sql, (self.username, self._hashed_password))
            self._id = cursor.fetchone()[0]
        else:
            sql = """
                  UPDATE users 
                  SET username=%s, hashed_password=%s 
                  WHERE id=%s;"""
            cursor.execute(sql, (self.username, self._hashed_password, self._id))

    @staticmethod
    def load_user_by_username(cursor, username):
        """
        Loads a user from the database by their username.
        :param cursor: The database cursor.
        :param username: The username to search for.
        :return: User object if found, None otherwise.
        """
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            user = User(username)
            user._id = id_
            user._hashed_password = hashed_password
            return user
        return None

    @staticmethod
    def load_user_by_id(cursor, id_):
        """
        Loads a user from the database by their id.
        :param cursor: The database cursor.
        :param id: The id to search for.
        :return: User object if found, None otherwise.
        """
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s;"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            user = User(username)
            user._id = id_
            user._hashed_password = hashed_password
            return user
        return None

    @staticmethod
    def load_all_users(cursor):
        """
        Loads all users from the database.
        :param cursor: The database cursor.
        :return: List of User objects.
        """
        sql = "SELECT id, username, hashed_password FROM users"
        cursor.execute(sql)
        users = []
        for id_, username, hashed_password in cursor.fetchall():
            user = User(username)
            user._id = id_
            user._hashed_password = hashed_password
            users.append(user)
        return users

    def delete(self, cursor):
        """
        Deletes a user from the database and resets their ID to -1.
        :param cursor: The database cursor.
        """
        if self._id != -1:
            sql = "DELETE FROM users WHERE id=%s;"
            cursor.execute(sql, (self._id,))
            self._id = -1





