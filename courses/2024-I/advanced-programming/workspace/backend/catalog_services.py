from typing import List
from fastapi import APIRouter
from core import Catalog, VideoGame

router_catalog = APIRouter()

@router_catalog.get("/catalog/get_categories", response_model=List[str])
def get_categories():
    """ hello """
    return Catalog.show_categories()

@router_catalog.get("/catalog/show_by_category/{category}", response_model=List[VideoGame])
def show_by_category(category: str):
    """ hello """
    return Catalog.show_by_category(category=category)

@router_catalog.get("/catalog/new_launches", response_model=List[VideoGame])
def new_launches():
    """ hello """
    return Catalog.show_new_launches()

@router_catalog.get("/catalog/all_games", response_model=List[VideoGame])
def show_catalog():
    """ hello """
    return Catalog.show_catalog()

@router_catalog.get("/catalog/game_by_code/{code}", response_model=VideoGame)
def show_by_code(code: int):
    """ hello """
    return Catalog.get_videogame(code)
