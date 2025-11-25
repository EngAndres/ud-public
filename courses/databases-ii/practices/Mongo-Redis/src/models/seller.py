from pydantic import BaseModel, EmailStr

class Seller(BaseModel):
    id: str
    name: str
    email: EmailStr
