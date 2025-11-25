from pydantic import BaseModel, Field
from typing import Optional

class ProductIn(BaseModel):
    id: int
    name: str = Field(..., min_length=5, max_length=20)
    price: float
    seller_code: int

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    price: float
    seller_name: str