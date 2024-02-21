# Corrected import for StaticFiles
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from typing import Optional
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import json
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = "tu_clave_de_api_aquí"

class RecommendationRequest(BaseModel):
    description: str

@app.post("/generate-recommendation/")
async def generate_recommendation(request: RecommendationRequest):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Asegúrate de utilizar el motor adecuado para tu caso de uso.
            prompt=f"Genera una recomendación basada en: {request.description}",
            max_tokens=50
        )
        return {"recommendation": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = "tu_clave_de_api_aquí"

class RecommendationRequest(BaseModel):
    description: str

@app.post("/generate-recommendation/")
async def generate_recommendation(request: RecommendationRequest):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Asegúrate de utilizar el motor adecuado para tu caso de uso.
            prompt=f"Genera una recomendación basada en: {request.description}",
            max_tokens=50
        )
        return {"recommendation": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
