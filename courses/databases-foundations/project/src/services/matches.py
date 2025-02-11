"""This module has the definitions for the endpoint related to matches information.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from connections.mysql_connection import MySQLDatabaseConnection
from crud.matches import MatchesCRUD
from dao import MatchData

router = APIRouter()

# Initialize MySQL DB connection and CRUD class.
db_connection = MySQLDatabaseConnection()
matches_crud = MatchesCRUD(db_connection)


@router.get("/matches", response_model=List[MatchData])
def get_all_matches():
    """
    Retrieve all matches from the database.

    Returns:
        List[MatchData]: A list of all match entries.
    """
    matches = matches_crud.get_all()
    return matches


@router.get("/matches/{id_match}", response_model=MatchData)
def get_match_by_id(id_match: int):
    """
    Retrieve a match given its id.

    Args:
        id_match (int): The ID of the match

    Raises:
        HTTPException: If no match is found with the given id.

    Returns:
        MatchData: The match data.
    """
    match = matches_crud.get_by_id(id_match)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match not found"
        )
    return match


@router.post("/matches", response_model=int)
def create_match(data: MatchData):
    """
    Create a new match entry in the database.

    Args:
        data (MatchData): The match data as defined in the MatchData model.

    Returns:
        int: The auto-generated id of the created match.
    """
    match_id = matches_crud.create(data)
    return match_id


@router.put("/matches/{id_match}", response_model=None)
def update_match(id_match: int, data: MatchData):
    """
    Update an existing match entry in the database.

    Args:
        id_match (int): The id of the match to update.
        data (MatchData): The updated match data.

    Raises:
        HTTPException: If the update process fails.
    """
    try:
        matches_crud.update(id_match, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update match"
        ) from e


@router.delete("/matches/{id_match}", response_model=None)
def delete_match(id_match: int):
    """
    Delete a match entry from the database.

    Args:
        id_match (int): The id of the match to delete.

    Raises:
        HTTPException: If the deletion process fails.
    """
    try:
        matches_crud.delete(id_match)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete match"
        ) from e
