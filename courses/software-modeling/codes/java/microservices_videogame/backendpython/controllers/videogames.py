"""This is a module to define some endpoints to handle videogames data.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from fastapi import APIRouter, HTTPException
from services.videogames import VideoGameServices, NameCategoryDTO
from repositories.videogames import VideoGamesDAO

router = APIRouter()

services = VideoGameServices()

@router.get("/videogames/all")        
def get_all() -> List[VideoGamesDAO]:
    """This method is used to get all videogames.
    """
    return services.get_all() 

@router.get("/videogames/by_name/{name}")    
def get_by_name(name: str) -> List[VideoGamesDAO]:
    """This method is used to get videogames by name.
    """
    if name == "":
        raise HTTPException(status_code=400, detail="The name cannot be empty.") 
    return services.get_by_name(name)

def get_by_category(category: str) -> List[VideoGamesDAO]:
    """This method is used to get videogames by category.
    """
    if category != "":
        return services.get_by_category(category)
    else:
        raise HTTPException(status_code=400, detail="The category cannot be empty.")

def get_by_price(min_price: float, max_price: float) -> List[VideoGamesDAO]:
    """This method is used to get videogames by price.
    """
    if min_price < max_price:
        return services.get_by_price(min_price, max_price)
    else:
        raise HTTPException(status_code=400, detail="The minimum price must be less than the maximum price.")

def get_by_description(self, keyword: str) -> List[VideoGamesDAO]:
    """This method is used to get videogames by description.
    """
    if keyword != "":
        return services.get_by_description(keyword)
    else:
        raise HTTPException(status_code=400, detail="The keyword cannot be empty.")

def get_by_name_category(self, data: NameCategoryDTO) -> List[VideoGamesDAO]:
    """This method is used to get videogames by name and category.
    NameCategoryDTO is expected to have name and category as fields.
    """
    if data.name != "" and data.category != "":
        return services.get_by_name_category(data)
    else:
        raise HTTPException(status_code=400, detail="The name and category cannot be empty.")
    