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

    def get_by_team(self, team_fk: int) -> List[PlayerData]:
        """This method gets all the players data from a specific team.

        Args:
            team_fk (int): The team code.

        Returns:
            A list of all the players data from the team.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                    team.name AS team_name 
            FROM player
            JOIN team ON player.team_fk = team.code
            WHERE team_fk = %s;
        """
        values = (team_fk,)
        return self.db_connection.get_many(query, values)

    def get_by_name(self, name: str) -> List[PlayerData]:
        """This method gets all the players data by name.

        Args:
            name (str): The name of the player.

        Returns:
            A list of all the players data by name.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                    team.name AS team_name 
            FROM player
            JOIN team ON player.team_fk = team.code
            WHERE LOWER(player.name) LIKE LOWER(%s);
        """
        values = (f"%{name}%",)
        return self.db_connection.get_many(query, values)

    def get_by_position(self, position: str) -> List[PlayerData]:
        """This method gets all the players data by position.

        Args:
            position (str): The position of the player.

        Returns:
            A list of all the players data by position.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                    team.name AS team_name 
            FROM player
            JOIN team ON player.team_fk = team.code
            WHERE LOWER(position) LIKE LOWER(%s);
        """
        values = (f"%{position}%",)
        return self.db_connection.get_many(query, values)

    def get_by_age(self, age: int) -> List[PlayerData]:
        """This method gets all the players data by age.

        Args:
            age (int): The age of the player.

        Returns:
            A list of all the players data by age.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                    team.name AS team_name 
            FROM player
            JOIN team ON player.team_fk = team.code
            WHERE age = %s;
        """
        values = (age,)
        return self.db_connection.get_many(query, values)

    def get_by_team_and_position(self, team_fk: int, position: str) -> List[PlayerData]:
        """This method gets all the players data by team and position.

        Args:
            team_fk (int): The team code.
            position (str): The position of the player.

        Returns:
            A list of all the players data by team and position.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                    team.name AS team_name 
            FROM player
            JOIN team ON player.team_fk = team.code
            WHERE team_fk = %s 
                AND LOWER(player.position) LIKE LOWER(%s);
        """
        values = (team_fk, f"%{position}%")
        return self.db_connection.get_many(query, values)

    def get_by_age_range(self, min_age: int, max_age: int) -> List[PlayerData]:
        """This method gets all the players data by team and age.

        Args:
            team_fk (int): The team code.
            age (int): The age of the player.

        Returns:
            A list of all the players data by team and age.
        """
        query = """
            SELECT player.id_player, player.name, player.age, player.position, player.team_fk,
                    team.name AS team_name 
            FROM player
            JOIN team ON player.team_fk = team.code
            WHERE player.age >= %s
                AND player.age <= %s;
        """
        values = (min_age, max_age)
        return self.db_connection.get_many(query, values)
