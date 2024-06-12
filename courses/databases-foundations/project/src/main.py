"""
This is the main file for the Youtube DB API.

Author: Carlos Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from fastapi import FastAPI
from sqlalchemy import Table, MetaData, create_engine, insert, update

from models import (
    Country,
    VideosCountry,
    ChannelCountry,
    Users,
    MusicalGenre,
    ReportUgly,
)

app = FastAPI(
    title="Youtube DB Example",
    description="This is a simple example of a Youtube DB API",
    version="0.2",
)

# db://ip:port@user:password/db_name
# postgres://localhost:5432@ud_admin:Admin12345/ud_db_project
# mysql://localhost:3306@root:P4ssw0rd/ud_project
db_connection = create_engine("mysql://root:P4ssw0rd@localhost:3306/ud_project")
metadata = MetaData()


@app.get("/")
def healthcheck():
    """This is a service to validate web API is up and running."""
    return {"status": "ok"}


@app.post("/country/add", status_code=201)
def add_country(country: Country):
    """This is a service to add a new country."""
    country_table = Table("country", metadata, autoload_with=db_connection)
    query = insert(country_table).values(code=country.code, name=country.name)
    with db_connection.connect() as connection:
        connection.execute(query)
    return {"message": "Country added successfully"}


@app.put("country/update/{country_code}")
def update_country(name: str, country_code: int):
    """This is a service to update a country name."""
    country_table = Table("country", metadata, autoload_with=db_connection)
    query = (
        update(country_table)
        .where(country_table.c.code == country_code)
        .values(name=name)
    )
    with db_connection.connect() as connection:
        connection.execute(query)
    return {"message": "Country updated successfully"}


@app.delete("country/delete/{country_code}")
def delete_country(country_code: int):
    """This is a service to delete a country."""
    country_table = Table("country", metadata, autoload_with=db_connection)
    query = country_table.delete().where(country_table.c.code == country_code)
    with db_connection.connect() as connection:
        connection.execute(query)
    return {"message": "Country deleted successfully"}


@app.get("/country/list", response_model=List[Country])
def list_countries() -> List[Country]:
    """This is a service to list all countries."""
    country_table = Table("country", metadata, autoload_with=db_connection)
    query = country_table.select()
    with db_connection.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()


@app.get("/video/by_country/{country_name}", response_model=List[VideosCountry])
def list_videos_by_country(country_name: str) -> List[VideosCountry]:
    """This is a service to list all videos by country."""
    with db_connection.connect() as connection:
        query = f"SELECT video.name, video.description, video.likes, \
                         video.dislikes, users.name AS user_name \
                FROM video \
                JOIN users ON video.user_fk = users.id_user  \
                JOIN country ON users.country_fk  = country.code \
                WHERE country.name LIKE '%{country_name}%';"
        result = connection.execute(query)
        return result.fetchall()


@app.get("/channels/by_country/{country_name}", response_model=List[ChannelCountry])
def list_channels_by_country(country_name: str) -> List[ChannelCountry]:
    """This is a service to list all channels by country."""
    with db_connection.connect() as connection:
        query = f"WITH subscribers_count AS ( \
                    SELECT count(*) AS counter, channel_fk  \
                    FROM subscribers_rel \
                    GROUP BY channel_fk \
                ) \
                SELECT channel.name, channel.description \
                FROM channel \
                JOIN subscribers_rel  \
                    ON subscribers_rel.channel_fk = channel.id_channel \
                JOIN users ON subscribers_rel.user_fk = users.id_user \
                JOIN country ON users.country_fk = country.code \
                JOIN subscribers_count  AS sc ON sc.channel_fk = channel.id_channel  \
                WHERE country.name LIKE '%{country_name}%' \
                    AND sc.counter >= 1;"
        result = connection.execute(query)
        return result.fetchall()


@app.get("/users/three_first", response_model=List[Users])
def list_users_three_first() -> List[Users]:
    """This is a service to list the first three users."""
    with db_connection.connect() as connection:
        query = "CALL three_users();"
        result = connection.execute(query)
        return result.fetchall()


@app.get("/musical-genre/all", response_model=List[MusicalGenre])
def list_musical_genre() -> List[MusicalGenre]:
    """This is a service to list all musical genres."""
    with db_connection.connect() as connection:
        query = "SELECT * FROM all_musical_genre;"
        result = connection.execute(query)
        return result.fetchall()


@app.get("/reports/ugly-word", response_model=List[ReportUgly])
def list_ugly_word() -> List[ReportUgly]:
    """This is a service to list all reports with ugly words."""
    with db_connection.connect() as connection:
        query = "SELECT * FROM view_report_ugly;"
        result = connection.execute(query)
        return result.fetchall()


@app.get("/video/popular")
def list_popular_videos():
    """This is a service to list the most popular videos."""
    with db_connection.connect() as connection:
        query = "SELECT * FROM view_popular_videos;"
        result = connection.execute(query)
        return result.fetchall()
