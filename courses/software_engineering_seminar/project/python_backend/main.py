"""Main entry point of the web rest api"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    """This method helps to validate if the web services are running fine."""
    return {"Message": "Services are up"}
