from typing import List, Optional
from  fastapi import APIRouter, HTTPException
from ..models import Seller
from ..services import SellerServices

router = APIRouter(prefix="/sellers", tags=["Sellers"])
seller_services = SellerServices()

@router.get("/get/{seller_id}", response_model=Optional[Seller])
async def get_seller(seller_id: str):
    seller = await seller_services.get_seller(seller_id)
    if not seller:
        raise HTTPException(status_code=404, 
                detail="El vendedor no existe en la base de datos.")
    return seller

@router.post("/new", status_code=201)
async def create_seller(seller: Seller):
    try:
        return await seller_services.create_seller(seller)
    except ValueError as e:
        raise HTTPException(status_code=400, 
                detail=f"Hubo un error almancenando al vendedor. {e}")
    
@router.get("/get_sellers/{skip}/{limit}", response_model=List[Seller])
async def get_sellers(skip: int, limit: int):
    return await seller_services.get_sellers(skip, limit)
