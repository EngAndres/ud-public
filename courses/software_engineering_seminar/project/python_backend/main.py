"""Main entry point of the web rest api"""

from fastapi import FastAPI
from src import calculator_router

app = FastAPI(
    title="UD Python Services",
    description="This is a set of simple web services for an online calculator.",
    version='0.2',
)
app.include_router(calculator_router)

@app.get("/healthcheck")
def healthcheck():
    """This method helps to validate if the web services are 
    running fine."""
    return {"Message": "Services are up"}
