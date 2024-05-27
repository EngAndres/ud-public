import uvicorn
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello_ud")
def hello_ud():
    return "Welcome to UD!"


engine = create_engine('postgresql://postgres:postgres@localhost:5432/public')
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('description', String))

app = FastAPI()


@app.get("/products")
def get_products():
    query = products.select()
    result = session.execute(query)
    products = result.fetchall()
    return products


@app.post("/products")
def create_product(name: str, description: str):
    query = products.insert().values(name=name, description=description)
    session.execute(query)
    session.commit()
    return {"message": "Product created successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
