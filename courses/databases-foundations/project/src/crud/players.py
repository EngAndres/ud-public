"""This module is responsible for performing CRUD operations on the player table.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List

from connections import DatabaseConnection
from dao import PlayerData


class PlayersCRUD:
    """This class is responsible for performing CRUD operations on the player table."""

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
        self.db_connection.connect()

    def create(self, data: PlayerData) -> int:
        """This method creates a new player in the database.

        Args:
            data (PlayerData): The player data.

        Returns:
            The persistend id of the new player.
        """
        query = """
            INSERT INTO player(id_player, name, age, position, team_fk)
            VALUES (%s, %s, %s, %s, %s);
        """
        values = (data.id_player, data.name, data.age, data.position, data.team_fk)
        return self.db_connection.create(query, values)

    def update(self, id_player: int, data: PlayerData):
        """This method updates the player data in the database.

        Args:
            id_player (int): The id of the player to be updated.
            data (PlayerData): The player data.
        """
        query = """
            UPDATE player
            SET name = %s, age = %s, position = %s, team_fk = %s 
            WHERE id_player = %s;
        """
        values = (data.name, data.age, data.position, data.team_fk, id_player)
        self.db_connection.update(query, values)

    def delete(self, id_player: int):
        """This method deletes the player from the database.

        Args:
            id_player (int): The id of the player.
        """
        query = """
        DELETE FROM player
        WHERE id_player = %s
        """
        self.db_connection.delete(query, id_player)

    def get_by_id(self, id_player: int) -> PlayerData:
        """This method gets a player from repository based on the id.

        Args:
            id_player (int): The id of the player.

        Returns:
            The player data.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                team.name AS team_name 
            FROM player 
            JOIN team ON player.team_fk = team.code
            WHERE id_player = %s;
        """
        values = (id_player,)
        return self.db_connection.get_one(query, values)

    def get_all(self) -> List[PlayerData]:
        """This method gets all the players data.

        Returns:
            A list of all the players data.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                    team.name AS team_name 
            FROM player
            JOIN team ON player.team_fk = team.code;
        """
        return self.db_connection.get_many(query)
