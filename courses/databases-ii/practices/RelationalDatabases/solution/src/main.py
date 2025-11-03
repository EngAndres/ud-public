"""Main application file for the World Demographic Info API."""

from fastapi import FastAPI
from routers import data_insertion_router, data_extraction_router

app = FastAPI(
    title="World Demographic Info",
    description="This is a set of endpoints to get demographic information using DDD architecture.",
    version="0.1.0"
)

# Include routers
app.include_router(data_insertion_router)
app.include_router(data_extraction_router)

@app.get("/", summary="Health check")
async def root():
    """Health check endpoint."""
    return {"message": "World Demographic API is running!"}
