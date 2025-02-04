from fastapi import FastAPI

from services.users import router as user_router

app = FastAPI(
    title="Users",
    version="0.0.1",
    description="This is an example of a CRUD using services."
)

app.include_router(user_router)