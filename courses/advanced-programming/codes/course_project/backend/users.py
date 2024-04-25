"""
This module contains the classes and methods to manage the users of the application.

Author: Carlo A. Sierra <cavirguezs@udistrital.edu.co>
"""

from membership import Membership
from bank_account import BankAccount
from news import News
from videogames import VideoGame


class User:
    """This class is an abstractation for any user into the application"""

    def __init__(self, name: str, alias: str, password: str, bank_account: BankAccount):
        self.name = name
        self.alias = alias
        self.password = password
        self.bank_account = bank_account
        self.grants = {}
        self.membership = Membership("free")

    @staticmethod
    def login(username: str, password: str):
        """
        This method is used to login into the application.

        Args:
            username (str): the alias of the user
            password (str): the password of the user
        """

    def can_publish(self):
        """
        This method is used to know if the user can publish a videogame
        """
        return self.grants.get("publish")


class Player(User):
    """This class represens a concrete implementation of a player user"""

    def __init__(
        self, age: int, name: str, alias: str, bank_account: BankAccount, password: str
    ):
        super().__init__(name, alias, password, bank_account)
        self.age = age
        self.bougth_videogames = []

    def buy_videogame(self, code):
        """
        This method is used to buy a videogame

        Args:
            code (str): the code of the videogame
        """
        videogame = Catalog.get_videogame(code)
        self.bougth_videogames.append(videogame)


class Seller(User):
    """This class represents a concrete implementation of a seller user"""

    def __init__(
        self,
        reputation: dict,
        name: str,
        alias: str,
        password: str,
        bank_account: BankAccount,
    ):
        super().__init__(name, alias, password, bank_account)
        self.reputation = reputation

    def publish_videogame(self, videogame: VideoGame) -> bool:
        """
        This function is used to publish a videogame.

        Args:
            videogame (VideoGame): the videogame to publish
        """
        if self.can_publish():
            return Catalog.add_videogame(videogame)
        else:
            return False

    def update_videogame(self, code: int, videogame: VideoGame) -> bool:
        """
        This function is used to update a videogame.

        Args:
            code (int): the code of the videogame
            videogame (VideoGame): the videogame to update
        """
        return Catalog.update_videogame(code, videogame)


class Manager(User):
    """This class represents a concrete implementation of a manager user"""

    def register_news(self, news: News):
        """
        This method is used to create a news.

        Args:
            news (News): the news to create.
        """
        # TODO: send to db

    def deactivate_news(self, news: News):
        """
        This method is used to deactivate a news.

        Args:
            news (News): the news to deactivate.
        """
        # TODO: update in db
