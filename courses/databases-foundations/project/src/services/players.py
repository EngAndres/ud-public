"""This module has the definitions for the endpoint related to players information.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from connections.mysql_connection import MySQLDatabaseConnection
from crud.players import PlayersCRUD
from dao import PlayerData

router = APIRouter()

# Initialize MySQL DB connection and Players CRUD instance.
db_connection = MySQLDatabaseConnection()
players_crud = PlayersCRUD(db_connection)


@router.get("/players/get_all", response_model=List[PlayerData])
def get_all_players():
    """
    Retrieve all players from the database.

    Returns:
        List[PlayerData]: A list of player data objects.
    """
    players = players_crud.get_all()
    return players


@router.get("/players/get_by_id/{id_player}", response_model=PlayerData)
def get_player_by_id(id_player: int):
    """
    Retrieve a player by its id.

    Args:
        id_player (int): The id of the player.

    Raises:
        HTTPException: If the player is not found.

    Returns:
        PlayerData: The player data object.
    """
    player = players_crud.get_by_id(id_player)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return player


@router.post("/players/create", response_model=int)
def create_player(data: PlayerData):
    """
    Create a new player in the database.

    Args:
        data (PlayerData): The player data.

    Returns:
        int: The auto-generated id of the new player.
    """
    player_id = players_crud.create(data)
    return player_id


@router.put("/players/update/{id_player}", response_model=dict)
def update_player(id_player: int, data: PlayerData):
    """
    Update an existing player's information.

    Args:
        id_player (int): The id of the player to update.
        data (PlayerData): The updated player data.

    Raises:
        HTTPException: If the player cannot be updated.

    Returns:
        dict: A success message.
    """
    try:
        players_crud.update(id_player, data)
        return {"detail": "Player updated successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update player"
        ) from exc


@router.delete("/players/delete/{id_player}", response_model=dict)
def delete_player(id_player: int):
    """
    Delete a player from the database.

    Args:
        id_player (int): The id of the player to delete.

    Raises:
        HTTPException: If the player cannot be deleted.

    Returns:
        dict: A success message.
    """
    try:
        players_crud.delete(id_player)
        return {"detail": "Player deleted successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete player"
        ) from exc


@router.get("/players/get_by_team/{team_fk}", response_model=List[PlayerData])
def get_players_by_team(team_fk: int):
    """
    Retrieve all players from a team.

    Args:
        team_fk (int): The id of the team.

    Returns:
        List[PlayerData]: A list of player data objects.
    """
    players = players_crud.get_by_team(team_fk)
    return players


@router.get("/players/get_by_name/{name}", response_model=List[PlayerData])
def get_players_by_name(name: str):
    """
    Retrieve all players by name.

    Args:
        name (str): The name of the player.

    Returns:
        List[PlayerData]: A list of player data objects.
    """
    players = players_crud.get_by_name(name)
    return players


@router.get("/players/get_by_position/{position}", response_model=List[PlayerData])
def get_players_by_position(position: str):
    """
    Retrieve all players by position.

    Args:
        position (str): The position of the player.

    Returns:
        List[PlayerData]: A list of player data objects.
    """
    players = players_crud.get_by_position(position)
    return players


@router.get("/players/get_by_age/{age}", response_model=List[PlayerData])
def get_players_by_age(age: int):
    """
    Retrieve all players by age.

    Args:
        age (int): The age of the player.

    Returns:
        List[PlayerData]: A list of player data objects.
    """
    players = players_crud.get_by_age(age)
    return players


@router.get(
    "/players/get_by_team_and_position/{team_fk}/{position}",
    response_model=List[PlayerData],
)
def get_players_by_team_and_position(team_fk: int, position: str):
    """
    Retrieve all players by team and position.

    Args:
        team_fk (int): The id of the team.
        position (str): The position of the player.

    Returns:
        List[PlayerData]: A list of player data objects.
    """
    players = players_crud.get_by_team_and_position(team_fk, position)
    return players


@router.get(
    "/players/get_by_age_range/{min_age}/{max_age}", response_model=List[PlayerData]
)
def get_players_by_age_range(min_age: int, max_age: int):
    """
    Retrieve all players by age range.

    Args:
        min_age (int): The minimum age of the player.
        max_age (int): The maximum age of the player.

    Returns:
        List[PlayerData]: A list of player data objects.
    """
    players = players_crud.get_by_age_range(min_age, max_age)
    return players
