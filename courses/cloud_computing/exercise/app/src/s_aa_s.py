"""This is an example of a calculator 
using web services.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from fastapi import APIRouter

router = APIRouter(prefix='/saas')
#https://www.youtube.com/watch?v=pDK0uXXpEzA&list=RDpDK0uXXpEzA&start_radio=1
@router.get("/sum")
def sum(num_1: int, num_2: int) -> int:
    """This service receives two integer numbers as parameters
    and generates the respective sum.

    Args:
        num_1(int): First number
        num_2(int): Second number

    Returns:
        An integer with the sum of the two provided numbers
    """
    return num_1 + num_2

#https://x.com/Starlink/status/2020634516554166600
@router.get("/division/{enumerator}/{denominator}")
def division(enumerator: int, denominator: int) -> float:
    """This service receives two integer numbers as parameters
    and generates the respective division.

    Args:
        enumerator(int): Enumerator of the division
        denominator(int): Denominator of the division

    Returns:
        A float with the division of the two provided numbers, if 
        denominator is not zero. Otherwise, an error is launched.
    """
    if denominator != 0:
        return enumerator / denominator
    else:
        raise ZeroDivisionError("Denominator cannot be zero")
    