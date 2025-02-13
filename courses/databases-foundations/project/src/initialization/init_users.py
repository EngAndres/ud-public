"""
This script creates a few users in the database.
It uses the Faker library to generate fake data for the users.
The script connects to the database, creates a CRUD instance,
and then creates a few users using the CRUD instance.
The script prints the ID of the created users.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from faker import Faker

from connections import DatabaseConnection
from dao import UserData
from crud.users import UsersCRUD


class InitUsers:
    """This class is responsible for creating users in the database."""

    def __init__(self, conn: DatabaseConnection):
        """This method initializes the class.

        Args:
            conn (DatabaseConnection): The database connection.
        """
        self.conn = conn

    def create_users(self, n: int) -> bool:
        """This method creates dummy users in the database.

        Args:
            n (int): The number of users to create.
            conn (DatabaseConnection): The database connection.
        """
        crud = UsersCRUD(self.conn)
        fake = Faker()

        try:
            for _ in range(n):
                id_user = -1
                username = fake.user_name()
                password = fake.password()
                email = fake.email()
                created_at = str(fake.date_this_month())
                data = UserData(
                    id_user=id_user,
                    username=username,
                    password=password,
                    email=email,
                    created_at=created_at,
                )
                user_id = crud.create(data)
                print(f"Created user with id: {user_id}")

            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
