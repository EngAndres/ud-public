"""This module contains a interface called DatabaseConnection in order
to define an structure indepent of the DBMS.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>"""

from typing import List

from dao import ProjectDAO


class DatabaseConnection:
    """This class is responsible for connecting to the database."""

    def connect(self):
        """This method connects to the database."""

    def disconnect(self):
        """This method connects to the database."""

    def list_schemas(self):
        """This method lists the schemas in the database."""

    def create(self, query: str, values: tuple) -> int:
        """This method creates a new item in the database.

        Args:
            query (str): The query to be executed.
            values (tuple): The values to be inserted.

        Returns:
            The auto-generated id of the new user
        """

    def update(self, query: str, values: tuple):
        """This method updates an item data in the database.

        Args:
            query (str): The query to be executed.
            values (tuple): The values to be inserted.
            item_id (int): The id of the item to be updated.
        """

    def delete(self, query: str, item_id: int):
        """This method deletes an item from a table in the  database
        based on the id.

        Args:
            query (str): The query to be executed.
            item_id (int): The id of the item to be deleted.
        """

    def get_one(self, query: str, values: tuple) -> ProjectDAO:
        """This method gets a on item from the repository based on any filter.

        Args:
            query (str): The query to be executed.
            values (tuple): The values to be added to the filter.

        Returns:
            The used who matched the filters.
        """

    def get_many(self, query: str, values: tuple = ()) -> List[ProjectDAO]:
        """This method get multiple elements from the repository

        Args:
            query (str): The query to be executed.
            values (tuple) [optional]: The values to be added to the filter

        Returns:
            A list with all the items of the database who matched the filter.
        """
