"""
This file contains the classes and methods to manage the memberships of players 
into the application.

Author: Carlo A. Sierra <cavirguezs@udistrital.edu.co>
"""

class Membership: #pylint: disable=too-few-public-methods
    """This class represents the behavior of a membership"""

    def __init__(self, name: str):
        self.name = name
