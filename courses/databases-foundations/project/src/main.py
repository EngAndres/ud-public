from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from sqlalchemy import create_engine

from country_models import Country, SubscriberByChannel

app = FastAPI(title="Youtube DB Example", description="This is a simple example of a Youtube DB API", version="0.2")

# db://ip:port@user:password/db_name
# postgres://localhost:5432@ud_admin:Admin12345/ud_db_project
# mysql://localhost:3306@root:P4ssw0rd/ud_project
db_connection = create_engine("mysql://root:P4ssw0rd@localhost:3306/ud_project")
db_client = db_connection.connect()

@app.get("/")
def healthcheck():
    """This is a service to validate web API is up and running."""
    return {"status": "ok"}

@app.post("/country/add", status_code=201)
def add_country(country: Country):
    """This is a service to add a new country."""
    query = f"INSERT INTO country(code, name) \
              VALUES({country.code}, {country.name})"
    print(country)
    db_client.execute(query)
    return None

@app.get("/susbcribers/country/{country_name}")
def get_subscribers_by_country() -> List[SubscriberByChannel]:
    """
    This is a service to get all channels with 
    at least one subscriber in a specific country.
    """
    query = "SELECT * FROM view_colombian_subscribe_channels;"
    return None

@app.put("country/update/{country_code}")
def update_country(name: str, country_code: int):
    """This is a service to update a country name."""
    query = f"UPDATE country SET name = {name} WHERE code = {country_code}"
    return None

@app.delete("country/delete/{country_code}")
def delete_country(country_code: int):
    """This is a service to delete a country."""
    query = f"DELETE FROM country WHERE code = {country_code}"
    return None