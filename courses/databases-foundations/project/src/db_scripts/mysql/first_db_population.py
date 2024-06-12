"""
This file is used to populate the country table in the ud_db_project database with fake data.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

import random
import uuid
from sqlalchemy import create_engine, Table, MetaData, select
from faker import Faker


# Create a Faker instance
fake = Faker()

# Create a SQLAlchemy engine
mysql_engine = create_engine(
    "mysql+mysqlconnector://root:P4ssw0rd@localhost:3306/ud_db_project"
)

# Initialize a metadata object
metadata = MetaData()

# =========================================================================================
# Reflect the country table
country = Table("country", metadata, autoload_with=mysql_engine)

# Start a new connection
with mysql_engine.connect() as connection:
    # Generate 10 fake country entries
    for _ in range(10):
        # Generate a fake country name
        country_name = fake.country()

        # Generate a random country code
        country_code = random.randint(1, 1000)

        # Insert the fake country into the database
        query = country.insert().values(code=country_code, name=country_name)
        connection.execute(query)

# =========================================================================================
# Reflect the musical_genre table
musical_genre = Table("musical_genre", metadata, autoload_with=mysql_engine)

# Start a new connection for MySQL
with mysql_engine.connect() as connection:
    # Generate 10 fake musical_genre entries
    for _ in range(10):
        # Generate a fake genre name and description
        genre_name = fake.word()[:15]  # Truncate to 15 characters
        genre_description = fake.text()[:100]  # Truncate to 100 characters

        # Insert the fake genre into the database
        query = musical_genre.insert().values(
            name=genre_name, description=genre_description
        )
        connection.execute(query)

# =========================================================================================
# Reflect the community table
community = Table("community", metadata, autoload_with=mysql_engine)

# Start a new connection for MySQL
with mysql_engine.connect() as connection:
    # Generate 10 fake community entries
    for _ in range(10):
        # Generate a fake community name and description
        community_name = fake.word()[:25]  # Truncate to 25 characters
        community_description = fake.text()[:200]  # Truncate to 200 characters

        # Insert the fake community into the database
        query = community.insert().values(
            name=community_name, description=community_description
        )
        connection.execute(query)

# =========================================================================================
# Reflect the users, musical_genre, and country tables
users = Table("users", metadata, autoload_with=mysql_engine)

# Start a new connection for MySQL
with mysql_engine.connect() as connection:
    # Get all genre ids and country codes
    genre_ids = connection.execute(select([musical_genre.c.id_genre])).fetchall()
    country_codes = connection.execute(select([country.c.code])).fetchall()

    # Generate 10 fake user entries
    for _ in range(10):
        # Generate a fake user details
        user_name = fake.name()[:50]  # Truncate to 50 characters
        user_email = fake.email()[:30]  # Truncate to 30 characters
        user_phone = fake.phone_number()[:50]  # Truncate to 50 characters
        user_nickname = fake.user_name()[:20]  # Truncate to 20 characters
        user_password = fake.password(length=30)
        user_musical_genre_fk = random.choice(genre_ids)[0]
        user_country_fk = random.choice(country_codes)[0]

        # Insert the fake user into the database
        query = users.insert().values(
            id_user=uuid.uuid4().bytes,
            name=user_name,
            email=user_email,
            phone=user_phone,
            nickname=user_nickname,
            password=user_password,
            musical_genre_fk=user_musical_genre_fk,
            country_fk=user_country_fk,
        )
        connection.execute(query)

# =========================================================================================
# Reflect the community_user_rel, community, and users tables
community_user_rel = Table('community_user_rel', metadata, autoload_with=mysql_engine)

# Start a new connection for MySQL
with mysql_engine.connect() as connection:
    # Get all community ids and user ids
    community_ids = connection.execute(select([community.c.id_community])).fetchall()
    user_ids = connection.execute(select([users.c.id_user])).fetchall()

    # Generate 10 fake community_user_rel entries
    for _ in range(10):
        # Generate a fake community_user_rel details
        community_fk = random.choice(community_ids)[0]
        user_fk = random.choice(user_ids)[0]
        expiration_date = fake.date_time_this_decade()

        # Insert the fake community_user_rel into the database
        query = community_user_rel.insert().values(community_fk=community_fk, user_fk=user_fk, expiration_date=expiration_date)
        connection.execute(query)

# =========================================================================================
# Reflect the playlist and users tables
playlist = Table('playlist', metadata, autoload_with=mysql_engine)

# Start a new connection for MySQL
with mysql_engine.connect() as connection:
    # Get all user ids
    user_ids = connection.execute(select([users.c.id_user])).fetchall()

    # Generate 10 fake playlist entries
    for _ in range(10):
        # Generate a fake playlist details
        playlist_name = fake.catch_phrase()[:30]  # Truncate to 30 characters
        playlist_likes = random.randint(0, 1000)
        user_fk = random.choice(user_ids)[0]

        # Insert the fake playlist into the database
        query = playlist.insert().values(name=playlist_name, likes=playlist_likes, user_fk=user_fk)
        connection.execute(query)
