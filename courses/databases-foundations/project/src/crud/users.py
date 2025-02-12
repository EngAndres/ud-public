"""This module contains the class UsersCRUD that is responsible for
performing CRUD operations on the users table.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List

from connections import DatabaseConnection
from dao import UserData


class UsersCRUD:
    """This class is responsible for performing CRUD operations
    on the users table.

    Attributes:
        db_connection (DatabaseConnection): The database connection

    Methods:
        create: Creates a new user in the database.
        update: Updates the user data in the database.
        delete: Deletes the user from the database.
        get_by_id: Gets a user from repository based on the id.
        get_all: Gets all the users data.
        get_by_name: Gets a user from repository based on the name.
        get_by_email: Gets a user from repository based on
    """

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
        self.db_connection.connect()

    def create(self, data: UserData) -> int:
        """This method creates a new user in the database.

        Args:
            data (UserData): The user data.

        Returns:
            The auto-generated id of the new user
        """
        query = """
            INSERT INTO football_auth.users(username, password, email, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id_user;
        """
        print(query)

        values = (data.username, data.password, data.email, data.created_at)
        print(values)
        return self.db_connection.create(query, values)

    def update(self, id_: int, data: UserData):
        """This method updates the user data in the database.

        Args:
            id (int): The id of the user to be updated.
            data (UserData): The user data.
        """
        query = """
            UPDATE football_auth.users
            SET username = %s, password = %s, email = %s, created_at = %s
            WHERE id_user = %s;
        """
        values = (data.username, data.password, data.email, data.created_at, id_)
        # The update method in pg_connection expects the id separately.
        self.db_connection.update(query, values)

    def delete(self, id_: int):
        """This method deletes the user from the database.

        Args:
            id (int): The id of the user to be deleted.
        """
        query = """
                DELETE FROM football_auth.users
                WHERE id_user = %s;
            """
        self.db_connection.delete(query, id_)

    def get_by_id(self, id_: int) -> UserData:
        """This method gets a user from repository
        based on the id.

        Args:
            id_ (int): Id of the user

        Returns:
            The used who matched the id.
        """
        query = """
            SELECT id_user, username, password, email, created_at
            FROM football_auth.users
            WHERE id_user = %s;
        """
        values = (id_,)
        return self.db_connection.get_one(query, values)

    def get_all(self) -> List[UserData]:
        """This method allows to get all the users data.

        Returns:
            A list with all the users of the database.
        """
        query = """
            SELECT id_user, username, password, email, created_at
            FROM football_auth.users;
        """
        return self.db_connection.get_many(query)

    def get_by_name(self, name: str):
        """This method gets a user from repository
        based on the name.

        Args:
            name (str): Name of the user

        Returns:
            The used who matched the name.
        """
        query = """
            SELECT id_user, username, password, email, created_at
            FROM football_auth.users
            WHERE username LIKE %s;
        """
        values = (f"%{name}%",)
        return self.db_connection.get_many(query, values)

    def get_by_email(self, email: str):
        """This method gets a user from repository
        based on the email.

        Args:
            email (str): Email of the user

        Returns:
            The used who matched the email.
        """
        query = """
            SELECT id_user, username, password, email, created_at
            FROM football_auth.users
            WHERE email = %s;
        """
        values = (email,)
        return self.db_connection.get_one(query, values)
