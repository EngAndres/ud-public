"""This module contains the CRUD operations for the stadium table.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List

from connections import DatabaseConnection
from dao import StadiumData


class StadiumsCRUD:
    """This class is responsible for performing CRUD operations on the stadium table."""

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
        self.db_connection.connect()

    def create(self, data: StadiumData) -> int:
        """This method creates a new stadium in the database.

        Args:
            data (StadiumData): The stadium data.

        Returns:
            The auto-generated id of the new stadium.
        """
        query = """
            INSERT INTO stadium(name, capacity, place)
            VALUES (%s, %s, %s)
            RETURNING id_stadium;
        """
        values = (data.name, data.capacity, data.place)
        return self.db_connection.create(query, values)

    def update(self, id_stadium: int, data: StadiumData):
        """This method updates the stadium data in the database.

        Args:
            id_stadium (int): The id of the stadium to be updated.
        """
        query = """
            UPDATE stadium
            SET name = %s, capacity = %s, place = %s
            WHERE id_stadium = %s;
        """
        values = (data.name, data.capacity, data.place, id_stadium)
        self.db_connection.update(query, values, id_stadium)

    def delete(self, id_stadium: int):
        """This method deletes the stadium from the database.

        Args:
            id_stadium (int): The id of the stadium.
        """
        self.db_connection.delete("stadium", id_stadium)

    def get_by_id(self, id_stadium: int) -> StadiumData:
        """This method gets a stadium from repository based on the id.

        Args:
            id_stadium (int): The id of the stadium.

        Returns:
            The stadium data.
        """
        query = """
            SELECT id_stadium, name, capacity, place 
            FROM stadium
            WHERE id_stadium = %s;
        """
        values = (id_stadium,)
        return self.db_connection.get_one(query, values)

    def get_all(self) -> List[StadiumData]:
        """This method gets all the stadiums data.

        Returns:
            A list of StadiumData objects.
        """
        query = """
            SELECT id_stadium, name, capacity, place 
            FROM stadium;
        """
        return self.db_connection.get_many(query)
