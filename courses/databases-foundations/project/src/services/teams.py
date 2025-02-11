"""This module has the definitions for the endpoint related to teams information.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from connections.mysql_connection import MySQLDatabaseConnection
from crud.teams import TeamsCRUD
from dao import TeamData

router = APIRouter()

# Initialize MySQL DB connection and Teams CRUD instance.
db_connection = MySQLDatabaseConnection()
teams_crud = TeamsCRUD(db_connection)


@router.get("/teams", response_model=List[TeamData])
def get_all_teams():
    """
    Retrieve all teams from the database.

    Returns:
        List[TeamData]: A list of all team data objects.
    """
    teams = teams_crud.get_all()
    return teams


@router.get("/teams/{code}", response_model=TeamData)
def get_team_by_code(code: int):
    """
    Retrieve a team by its code.

    Args:
        code (int): The code of the team.

    Raises:
        HTTPException: If the team is not found.

    Returns:
        TeamData: The team data object.
    """
    team = teams_crud.get_by_code(code)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@router.post("/teams", response_model=int)
def create_team(data: TeamData):
    """
    Create a new team in the database.

    Args:
        data (TeamData): The team data.

    Returns:
        int: The persisted code of the new team.
    """
    team_code = teams_crud.create(data)
    return team_code


@router.put("/teams/{code}")
def update_team(code: int, data: TeamData):
    """
    Update a team's information.

    Args:
        code (int): The code of the team to update.
        data (TeamData): The updated team data.

    Raises:
        HTTPException: If the team cannot be updated.

    Returns:
        dict: A message indicating successful update.
    """
    try:
        teams_crud.update(code, data)
        return {"detail": "Team updated successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update team"
        ) from exc


@router.delete("/teams/{code}")
def delete_team(code: int):
    """
    Delete a team from the database.

    Args:
        code (int): The code of the team to delete.

    Raises:
        HTTPException: If the team cannot be deleted.

    Returns:
        dict: A message indicating successful deletion.
    """
    try:
        teams_crud.delete(code)
        return {"detail": "Team deleted successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete the team"
        ) from exc
