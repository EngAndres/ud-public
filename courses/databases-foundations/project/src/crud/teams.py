"""This module contains the CRUD operations for the team table.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co
"""

from typing import List

from connections import DatabaseConnection
from dao import TeamData


class TeamsCRUD:
    """This class is responsible for performing CRUD operations on the team table."""

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
        self.db_connection.connect()

    def create(self, data: TeamData) -> int:
        """This method creates a new team in the database.

        Args:
            data (TeamData): The team data.

        Returns:
            The perdisted id (code) of the new team.
        """
        query = """
            INSERT INTO team(code, name, color, coach)
            VALUES (%s, %s, %s, %s)
            RETURNING code;
        """
        values = (data.code, data.name, data.color, data.coach)
        return self.db_connection.create(query, values)

    def update(self, code: int, data: TeamData):
        """This method updates the team data in the database.

        Args:
            code (int): The code of the team to be updated.
            data (TeamData): The team data.
        """
        query = """
            UPDATE team 
            SET name = %s, color = %s, coach = %s
            WHERE code = %s;
        """
        values = (data.name, data.color, data.coach, code)
        self.db_connection.update(query, values, code)

    def delete(self, code: int):
        """This method deletes the team from the database.

        Args:
            code (int): The code of the team.
        """
        self.db_connection.delete("team", code)

    def get_by_code(self, code: int) -> TeamData:
        """This method gets a team from repository based on the code.

        Args:
            code (int): The code of the team.

        Returns:
            The team data.
        """
        query = """
            SELECT code, name, color, coach 
            FROM team
            WHERE code = %s;
        """
        values = (code,)
        return self.db_connection.get_one(query, values)

    def get_all(self) -> List[TeamData]:
        """This method gets all teams from the repository.

        Returns:
            A list of all teams.
        """
        query = """
            SELECT code, name, color, coach 
            FROM team;
        """
        return self.db_connection.get_many(query)
