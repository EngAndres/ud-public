"""This is a set of web services to connect
to different data sources to retrieve information.

Author: Carlos Andrés Sierra <cavisrguezs@udistrital.edu.co
"""

from fastapi import APIRouter

router = APIRouter(prefix="/extract")

@router.get("/historial")
def historial():
    return "All data"

@router.get("/today")
def today():
    return "Today data"