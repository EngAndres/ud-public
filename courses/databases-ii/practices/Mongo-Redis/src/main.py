"""This is the entry point of the app."""

from fastapi import FastAPI

app = FastAPI(title="E-Commerce UD")

@app.get("/healthcheck")
def healthcheck():
    return {"Message": "E-Commerce UD is up."}
