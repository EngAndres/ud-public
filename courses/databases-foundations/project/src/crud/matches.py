"""This module is responsible for performing CRUD operations on the match table.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List

from connections import DatabaseConnection
from dao import MatchData


class MatchesCRUD:
    """This class is responsible for performing CRUD operations on the match table."""

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
        self.db_connection.connect()

    def create(self, data: MatchData) -> int:
        """This method creates a new match in the database.

        Args:
            data (MatchData): The match data.

        Returns:
            The auto-generated id of the new match
        """
        query = """
            INSERT INTO `match` (id_match, match_date, local_fk, guest_fk, score_local, score_guest)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_match;
        """
        values = (
            data.id_match,
            data.match_date,
            data.local_fk,
            data.guest_fk,
            data.score_local,
            data.score_guest,
        )
        return self.db_connection.create(query, values)

    def update(self, id_match: int, data: MatchData):
        """This method updates the match data in the database.

        Args:
            id_match (int): The id of the match to be updated.
            data (MatchData): The match data.
        """
        query = """
            UPDATE `match`
            SET match_date = %s, score_local = %s, score_guest = %s
            WHERE id_match = %s;
        """
        values = (
            data.match_date,
            data.score_local,
            data.score_guest,
            id_match,
        )
        self.db_connection.update(query, values, id_match)

    def delete(self, id_match: int):
        """This method deletes the match from the database.

        Args:
            id_match (int): The id of the match to be deleted.
        """
        self.db_connection.delete("`match`", id_match)

    def get_by_id(self, id_match: int) -> MatchData:
        """This method gets a match from repository based on the id.

        Args:
            id_match (int): Id of the match

        Returns:
            The match data
        """
        query = """
            SELECT id_match, match_date, local_fk, guest_fk, score_local, score_guest
            FROM `match`
            WHERE id_match = %s;
        """
        values = (id_match,)
        return self.db_connection.get_one(query, values)

    def get_all(self) -> List[MatchData]:
        """This method allows to get all the matches data.

        Returns:
            A list with all the matches of the database.
        """
        query = """
            SELECT id_match, match_date, local_fk, guest_fk, score_local, score_guest
            FROM `match`;
        """
        return self.db_connection.get_many(query)
