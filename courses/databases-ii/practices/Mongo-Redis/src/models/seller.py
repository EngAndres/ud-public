from pydantic import BaseModel, EmailStr

class Seller(BaseModel):
    id: int
    name: str
    email: EmailStr
