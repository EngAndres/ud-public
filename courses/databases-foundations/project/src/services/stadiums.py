"""This module has the definitions for the endpoint related to stadiums information.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from connections.mysql_connection import MySQLDatabaseConnection
from crud.stadiums import StadiumsCRUD
from dao import StadiumData

router = APIRouter()

# Initialize MySQL DB connection and CRUD class.
db_connection = MySQLDatabaseConnection()
stadiums_crud = StadiumsCRUD(db_connection)


@router.get("/stadiums/get_all", response_model=List[StadiumData])
def get_all_stadiums():
    """
    Retrieve all stadiums from the database.

    Returns:
        List[StadiumData]: A list of stadium data objects.
    """
    stadiums = stadiums_crud.get_all()
    return stadiums


@router.get("/stadiums/get_by_id/{id_stadium}", response_model=StadiumData)
def get_stadium_by_id(id_stadium: int):
    """
    Retrieve a stadium by its id.

    Args:
        id_stadium (int): The id of the stadium.

    Raises:
        HTTPException: If the stadium is not found.

    Returns:
        StadiumData: The stadium data object.
    """
    stadium = stadiums_crud.get_by_id(id_stadium)
    if not stadium:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stadium not found"
        )
    return stadium


@router.post("/stadiums/create", response_model=int)
def create_stadium(data: StadiumData):
    """
    Create a new stadium in the database.

    Args:
        data (StadiumData): The stadium data.

    Returns:
        int: The auto-generated id of the new stadium.
    """
    stadium_id = stadiums_crud.create(data)
    return stadium_id


@router.put("/stadiums/update/{id_stadium}")
def update_stadium(id_stadium: int, data: StadiumData):
    """
    Update a stadium's information.

    Args:
        id_stadium (int): The id of the stadium to update.
        data (StadiumData): The updated stadium data.

    Raises:
        HTTPException: If the stadium cannot be updated.
    """
    try:
        stadiums_crud.update(id_stadium, data)
        return {"detail": "Stadium updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update stadium"
        ) from e


@router.delete("/stadiums/delete/{id_stadium}")
def delete_stadium(id_stadium: int):
    """
    Delete a stadium from the database.

    Args:
        id_stadium (int): The id of the stadium to delete.

    Raises:
        HTTPException: If the stadium cannot be deleted.
    """
    try:
        stadiums_crud.delete(id_stadium)
        return {"detail": "Stadium deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete stadium"
        ) from e


@router.get("/stadiums/get_by_place/{place}", response_model=List[StadiumData])
def get_stadium_by_place(place: str):
    """
    Retrieve a stadium by its place.

    Args:
        place (str): The place of the stadium.

    Raises:
        HTTPException: If the stadium is not found.

    Returns:
        StadiumData: The stadium data object.
    """
    stadium = stadiums_crud.get_by_place(place)
    if not stadium:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stadium not found"
        )
    return stadium


@router.get("/stadiums/get_by_capacity/{capacity}", response_model=List[StadiumData])
def get_stadium_by_capacity(capacity: int):
    """
    Retrieve a stadium by its capacity.

    Args:
        capacity (int): The capacity of the stadium.

    Raises:
        HTTPException: If the stadium is not found.

    Returns:
        StadiumData: The stadium data object.
    """
    stadium = stadiums_crud.get_by_capacity(capacity)
    if not stadium:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stadium not found"
        )
    return stadium


@router.get("/stadiums/get_by_name/{name}", response_model=List[StadiumData])
def get_stadium_by_name(name: str):
    """
    Retrieve a stadium by its name.

    Args:
        name (str): The name of the stadium.

    Raises:
        HTTPException: If the stadium is not found.

    Returns:
        StadiumData: The stadium data object.
    """
    stadium = stadiums_crud.get_by_name(name)
    if not stadium:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stadium not found"
        )
    return stadium
