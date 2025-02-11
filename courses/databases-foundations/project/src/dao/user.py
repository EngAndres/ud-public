"""This module is responsible for defining the user data structure.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from dao.project_dao import ProjectDAO


class UserData(ProjectDAO):
    """This class is responsible for defining the user data structure."""

    id_user: int = -1
    username: str
    password: str
    email: str
    created_at: str
