"""This file  has theentry point implementtion for RESTapi services."""
from typing import List
from fastapi import FastAPI
from users_sub import User, Player, Seller, Manager
from news import News
from core import VideoGame, Catalog
from community import Community
from models import UserCredentials

from catalog_services import router_catalog

app = FastAPI()
app.include_router(router_catalog)



@app.post("/login", response_model=User)
def login(credentials: UserCredentials):
    """
    This method validates if a user is valid or not.

    Args:
        credentials (dict): username and password of the user
    """
    return User.login(credentials.username, credentials.password)

@app.post("/create_player")
def create_player(player: Player) -> bool:
    """
    This method lets create a new player.

    Args:
        player (Player): player to be added
    """
    # TODO add Player to DB

@app.post("/create_seller")
def create_seller(seller: Seller) -> bool:
    """
    This method lets create a new seller.

    Args:
        seller (Seller): seller to be added
    """
    # TODO add Player to DB

@app.post("/create_manager")
def create_manager(manager: Manager) -> bool:
    """
    This method lets create a new manager.

    Args:
        manager (Manager): manager to be added
    """
    # TODO add Player to DB

@app.patch("/manager/mark_videogame/{code}")
def mark_videogame(code: int) -> bool:
    """This is a service to mark a videogame as a new launch."""
    manager = Manager()
    return manager.mark_videogame(code)

@app.post("/manager/register_platform_news")
def register_plaftorm_news(news: News):
    """This service lets to add a news in the platform."""
    manager = Manager(name="name", alias="alias", password="password", grants={})
    manager.register_news(news)

@app.put("/manage/deactivate_platform_news")
def deactivate_platform_news(news: News):
    """This service lets deactivate a news"""
    # TODO db and change news status

@app.post("/player/buy_videogame", response_model=VideoGame)
def buy_videogame(data: dict):
    """This service lets a user to by a videogame"""
    user = User()
    user.buy_videogame(data["code"])

@app.post("/seller/publish_videogame")
def publish_videogame(videogame: VideoGame):
    """This service lets add a new videogame to the catalog"""
    Catalog.add_videogame(videogame)

@app.put("/seller/update_videogame/{code}")
def update_videogame(code: int, videogame: VideoGame): 
    manager = Manager()
    manager.update_videogame(code, videogame)

@app.post("/player/create_community")
def create_community(community: Community):
    # TODO add community to db
    pass
