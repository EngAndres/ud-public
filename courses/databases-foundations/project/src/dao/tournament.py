"""This module contains the data classes for the tournament project.
These classes are used to define the data structures used in the project.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import Optional

from dao.project_dao import ProjectDAO


class TeamData(ProjectDAO):
    """DAO for team data."""

    code: int = -1
    name: str
    color: Optional[str] = None
    coach: str


class PlayerData(ProjectDAO):
    """DAO for player data."""

    id_player: int = -1
    name: str
    age: int
    position: Optional[str] = None
    team_fk: int
    team_name: Optional[str] = None


class MatchData(ProjectDAO):
    """DAO for match data."""

    id_match: int = -1
    match_date: str
    local_fk: int
    guest_fk: int
    score_local: Optional[int] = None
    score_guest: Optional[int] = None


class StadiumData(ProjectDAO):
    """DAO for stadium data."""

    id_stadium: int = -1
    name: str
    capacity: int
    place: str
