from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(title="SD-Project")
api.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1", "localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/", status_code=200)
def hello_project():
    return "This is an RESTful api"
                                                                           