"""This module has the endpoints associated to a simple
calculator.

Author: Carlos Andres Sierra <cavirguesz@udistrital.edu.co>"""

from fastapi import APIRouter
from ..models import Input
from ..services import Calculator

router = APIRouter()
calculator = Calculator()

@router.post("/sum")
def sum_endpoint(numbers: Input):
    """This service allows a typical sum of two numbers."""
    return {"response": calculator.sum(numbers.num_1, numbers.num_2)}

@router.post("/division")
def division_endpoint(numbers: Input):
    """This service allows a typical divison of two numbers."""
    return {"response": calculator.division(numbers.num_1, numbers.num_2)}
