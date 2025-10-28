from fastapi import FastAPI
from models import Country

app = FastAPI(title="World Demographic Info",
    description="This is a set of endpoints to get demographic information.",
    version=0.1)

@app.post('/add_country')
def add_country(country: Country):
    pass