"""
This is a module with some simple web services using FastAPI.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

import os
import uvicorn
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(
    f"postgresql://\
    {os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}\
    @{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("description", String),
)

app = FastAPI()


origins = ["http://localhost", "http://localhost:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello_ud")
def hello_ud():
    """This is a healthcheck service just to validade is backend is up"""
    return "Welcome to UD!"


@app.get("/products")
def get_products():
    """
    This service returns all the products stored
    in the database
    """
    global products
    query = products.select()
    result = session.execute(query)
    products = result.fetchall()
    return products


@app.post("/products")
def create_product(name_arg: str, description_arg: str):
    """This method creates a product inside the database"""
    query = products.insert().values(name=name_arg, description=description_arg)
    session.execute(query)
    session.commit()
    return {"message": "Product created successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
