"""
Router for data insertion endpoints.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from fastapi import APIRouter, HTTPException
from models import CountryWithLanguage, CityCreate
from services import CountryService, CityService

router = APIRouter(prefix="/data", tags=["Data Insertion"])


@router.post("/add_country", summary="Add a new country with language.")
async def add_country(country: CountryWithLanguage):
    """Add a new country including its language information."""
    service = CountryService()
    try:
        success = service.add_country_with_language(country)
        if success:
            return {
                "message": "Country and language added successfully",
                "country_code": country.code,
            }

        raise HTTPException(status_code=500, detail="Failed to add country")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error adding country: {str(e)}"
        ) from e


@router.post("/add_city", summary="Add a new city.")
async def add_city(city: CityCreate):
    """Add a new city and relate it to a country."""
    service = CityService()
    try:
        success = service.add_city(city)
        if success:
            return {"message": "City added successfully", "city_name": city.name}
        
        raise HTTPException(status_code=500, detail="Failed to add city")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error adding city: {str(e)}"
        ) from e
