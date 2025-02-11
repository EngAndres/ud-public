"""This module contains the services related to the users in the database."""

from typing import List
from fastapi import APIRouter

from dao import UserData
from crud import UsersCRUD
from initialization import InitUsers


from connections import PostgresDatabaseConnection


router = APIRouter()
conn = PostgresDatabaseConnection()
crud = UsersCRUD(conn)
init = InitUsers(conn)


@router.post("/user/create", response_model=int)
def create(data: UserData):
    """This service creates a new user in the database.
    Remember that the user data must have the specified struture."""
    return crud.create(data)


@router.put("/user/update/{id_}", response_model=UserData)
def update(id_: int, data: UserData):
    """This service updates the user data in the database based on its id."""
    return crud.update(id_, data)


@router.delete("/user/delete/{id_}", response_model=bool)
def delete(id_: int):
    """This service deletes a user from the database based on its id."""
    return crud.delete(id_)


@router.get("/user/get_by_id/{id_}", response_model=UserData)
def get_by_id(id_: int):
    """This service gets a user from the database based on its id."""
    return crud.get_by_id(id_)


@router.get("/user/get_all", response_model=List[UserData])
def get_all():
    """This service gets all the users from the database."""
    return crud.get_all()


@router.get("/user/get_by_name/{name}", response_model=List[UserData])
def get_by_name(name: str):
    """This service gets a user from the database based on its name."""
    return crud.get_by_name(name)


@router.get("/user/get_by_email/{email}", response_model=UserData)
def get_by_email(email: str):
    """This service gets a user from the database based on its email."""
    return crud.get_by_email(email)


@router.get("/user/generate_fake_users/{n}", response_model=bool)
def generate_fake_users(n: int):
    """This service generates n fake users in the database."""
    return init.create_users(n)
