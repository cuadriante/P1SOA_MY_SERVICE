# Corrected import for StaticFiles
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from typing import Optional
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import json

app = FastAPI()

class RecommendationInput(BaseModel):
    type: str  # Could be 'dessert', 'main_course', 'drink'
    preferences: Optional[str] = None  # Additional preferences like 'gluten-free'

@app.post("/recommend/")
async def recommend(input: RecommendationInput):
    return {"message": f"Recommendation for {input.type} with preferences: {input.preferences}"}

@app.get("/")
async def root():
    return {"message": "Welcome to the recommendation service"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom Recommendation Service",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.on_event("startup")
async def startup_event():
    openapi_schema = custom_openapi()
    with open('static/openapi.json', 'w') as file:
        json.dump(openapi_schema, file)

app.openapi = custom_openapi

# Mounting the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
