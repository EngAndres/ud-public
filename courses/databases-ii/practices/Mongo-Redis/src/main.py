"""This is the entry point of the app."""

from fastapi import FastAPI
from api import sellers_router
app = FastAPI(title="E-Commerce UD")

app.include_router(sellers_router)

@app.get("/healthcheck")
def healthcheck():
    return {"Message": "E-Commerce UD is up."}
