"""This module is used to initialize the tournament.

Author: Carlos Andres Sierra <cavirguesz@udistrital.edu.co
"""

from connections import MySQLDatabaseConnection
from crud import TeamsCRUD, PlayersCRUD, StadiumsCRUD, MatchesCRUD
from dao import TeamData, PlayerData, StadiumData, MatchData


class InitTournament:
    """This class is just used to add information into the db."""

    def __init__(self):
        mysql_conn = MySQLDatabaseConnection()
        self.teams_crud = TeamsCRUD(mysql_conn)
        self.players_crud = PlayersCRUD(mysql_conn)
        self.stadiums_crud = StadiumsCRUD(mysql_conn)
        self.matches_crud = MatchesCRUD(mysql_conn)

    def create_data(self):
        """This method is used to create the data."""
        self._create_teams()
        self._create_players()
        self._create_stadiums()

    def _create_teams(self):
        """This method is used to create the teams."""
        print("Creating teams...")
        self.teams_crud.create(
            TeamData(code=123, name="Libre&Pool", color="Rojo", coach="Jurguen Klopp")
        )

        print("Creating teams...")
        self.teams_crud.create(
            TeamData(
                code=124, name="Farcelona", color="Bulgrana", coach="Ronald Koeman"
            )
        )
        self.teams_crud.create(
            TeamData(
                code=125, name="Aston Huila", color="Vinotinto", coach="Dean Smith"
            )
        )
        self.teams_crud.create(
            TeamData(
                code=126, name="Real Madrazo", color="Blanco", coach="Zinedine Zidane"
            )
        )

    def _create_players(self):
        """This method is used to create the players."""
        print("Creating players...")
        # Libre&Pool
        self.players_crud.create(
            PlayerData(
                id_player=123451,
                name="Mohamed Salah",
                age=29,
                position="Delantero",
                team_fk=123,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123452,
                name="Virgil Van Dijk",
                age=30,
                position="Defensa",
                team_fk=123,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123453,
                name="Sadio Mane",
                age=29,
                position="Delantero",
                team_fk=123,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123454,
                name="Alisson Becker",
                age=28,
                position="Portero",
                team_fk=123,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123455, name="Fabinho", age=27, position="Medio", team_fk=123
            )
        )
        # Farcelona
        self.players_crud.create(
            PlayerData(
                id_player=123456,
                name="Lionel Messi",
                age=33,
                position="Delantero",
                team_fk=124,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123457,
                name="Gerard Pique",
                age=34,
                position="Defensa",
                team_fk=124,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123458,
                name="Sergio Busquets",
                age=32,
                position="Medio",
                team_fk=124,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123459,
                name="Ansu Fati",
                age=18,
                position="Delantero",
                team_fk=124,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123460,
                name="Marc-Andre Ter Stegen",
                age=29,
                position="Portero",
                team_fk=124,
            )
        )
        # Aston Huila
        self.players_crud.create(
            PlayerData(
                id_player=123461,
                name="Ollie Watkins",
                age=25,
                position="Delantero",
                team_fk=125,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123462,
                name="Jack Grealish",
                age=25,
                position="Medio",
                team_fk=125,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123463,
                name="Emiliano Martinez",
                age=28,
                position="Portero",
                team_fk=125,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123464,
                name="Tyrone Mings",
                age=28,
                position="Defensa",
                team_fk=125,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123465,
                name="John McGinn",
                age=26,
                position="Medio",
                team_fk=125,
            )
        )
        # Reak Madrazo
        self.players_crud.create(
            PlayerData(
                id_player=123461,
                name="Karim Benzema",
                age=33,
                position="Delantero",
                team_fk=126,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123462,
                name="Luka Modric",
                age=35,
                position="Medio",
                team_fk=126,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123463,
                name="Sergio Ramos",
                age=35,
                position="Defensa",
                team_fk=126,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123464,
                name="Thibaut Courtois",
                age=29,
                position="Portero",
                team_fk=126,
            )
        )
        self.players_crud.create(
            PlayerData(
                id_player=123465, name="Casemiro", age=29, position="Medio", team_fk=126
            )
        )

    def _create_stadiums(self):
        """This method is used to create the stadiums."""
        print("Create Stadiums...")

        self.stadiums_crud.create(
            StadiumData(id_stadium=1, name="Anfield", capacity=54074, place="Liverpool")
        )
        self.stadiums_crud.create(
            StadiumData(
                id_stadium=2, name="Camp Nou", capacity=99354, place="Barcelona"
            )
        )
        self.stadiums_crud.create(
            StadiumData(
                id_stadium=3, name="Villa Park", capacity=42788, place="Birmingham"
            )
        )
        self.stadiums_crud.create(
            StadiumData(
                id_stadium=4, name="Santiago Bernabeu", capacity=81044, place="Madrid"
            )
        )
