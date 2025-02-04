"""This module contains the class UsersCRUD that is responsible for
performing CRUD operations on the users table.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from pydantic import BaseModel

from database_connection import PostgresDatabaseConnection


class UserData(BaseModel):
    """This class is responsible for defining the user data structure."""
    id_user: int
    username: str
    password: str
    email: str
    created_at: str


class UsersCRUD:

    def __init__(self):
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execution(self, query: str, values: tuple):
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            self.db_connection.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Failing in the user update. {e}")


    def create(self, data: UserData) -> int:
        """This method creates a new user in the database.
        
        Args:
            data (UserData): The user data.

        Returns:
            The auto-generated id of the new user
        """
        query = """
            INSERT INTO condor.users(username, password, email, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id_user;
        """
        try:
            values = (data.username, data.password, data.email, data.created_at)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return user_id
        except Exception as e:
            print(f"Failing in the user update. {e}")


    def update(self, id_: int, data: UserData):
        """This method updates the user data in the database.
        
        Args:
            id (int): The id of the user to be updated.
            data (UserData): The user data.
        """
        query = """
            UPDATE condor.users
            SET username = %s, password = %s
            WHERE id_user = %s;
        """
        try:
            values = (data.username, data.password, id_)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the user update. {e}")

    def delete(self, id_: int):
        """This method deletes the user from the database.

        Args:
            id (int): The id of the user to be deleted.
        """
        query = """
            DELETE FROM condor.users
            WHERE id_user = %s;
        """
        try:
            values = (id_,)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the user delete. {e}")

    def get_by_id(self, id_: int) -> UserData:
        """This method gets a user from repository
        based on the id.

        Args:
            id_ (int): Id of the user
        
        Returns:
            The used who matched the id.
        """
        query = """
            SELECT username, password, email, created_at
            FROM condor.users
            WHERE id_user = %s;
        """
        try:
            values = (id_, )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"Failing to get user by id. {e}")

    def get_all(self) -> List(UserData):
        """This method allows to get all the users data.

        Returns:
            A list with all the users of the database.
        """
        query = """
            SELECT *
            FROM condor.users;
        """
        users = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            users = cursor.fetchall()
        except Exception as e:
            print(f"Fail getting all the users. {e}")

        return users

    def get_by_name(self, name: str):
        query = """
            SELECT id_user, username, password, email, created_at
            FROM condor.users
            WHERE username LIKE '\% %s \%';
        """
        try:
            values = (name, )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Fail getting users by name. {e}")

    def get_by_email(self, email: str):
        query = """
            SELECT id_user, username, password, email, created_at
            FROM condor.users
            WHERE email = %s;
        """
        try:
            values = (email, )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Fail getting a user by email. {e}")
