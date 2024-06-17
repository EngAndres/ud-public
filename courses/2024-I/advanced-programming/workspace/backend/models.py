from pydantic import BaseModel

class UserCredentials(BaseModel):
    username: str
    password: str