"""
This module has a definition of the Student model.

Author: Carlos Andres Sierra <cavirguezs@udistrial.edu.co>
"""

from pydantic import BaseModel

class Student(BaseModel):
    """This cla
    ss represents a Student model."""
    code: int
    name: str
    email: str
    phone: str
    address: str
    career: str
