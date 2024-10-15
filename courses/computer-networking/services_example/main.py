from fastapi import FastAPI

api = FastAPI() # Create a FastAPI instance

@api.get("/")
def healthcheck():
    return {"status": "I'am allive"}

@api.get("/hello_UD")
def hello_ud():
    message = {"date": "2021-09-01", 
               "message": "Hello UD students",
               "class": "Computer Networking"}
    return message