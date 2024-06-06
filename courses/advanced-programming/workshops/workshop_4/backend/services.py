"""
This is a module with some simple web services using FastAPI.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

import os
from typing import List
import uvicorn
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("description", String, default="No available"),
)
metadata.create_all(engine)

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

class Product(BaseModel):
    id: int = None
    name: str
    description: str



@app.get("/products")
def get_products() -> List[Product]:
    """
    This service returns all the products stored
    in the database
    """
    global products
    query = products.select()
    result = session.execute(query)
    products = result.fetchall()

    return products


@app.post("/products/add")
def create_product(product: Product):
    """This method creates a product inside the database"""
    print(product)
    query = products.insert().values(name=product.name, description=product.description)
    session.execute(query)
    session.commit()
    return {"message": "Product created successfully"}


if __name__ == "__main__":
    product = Product(name="Product 3", description="This is a product 2")
    print(create_product(product))
    uvicorn.run(app, host="0.0.0.0", port=8080)
