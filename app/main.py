from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from starlette.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
import json

# Carga las variables de entorno desde un archivo .env en el directorio actual
load_dotenv()

app = FastAPI()

# Configura el cliente de OpenAI con la clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")

class RecommendationRequest(BaseModel):
    description: str

@app.post("/generate-recommendation/")
async def generate_recommendation(request: RecommendationRequest):
    try:
        # Inicializa el cliente de OpenAI con la clave de API
        client = openai.OpenAI(api_key=openai.api_key)
        
        # Realiza la solicitud de completion de chat
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": request.description,
                },
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
            ],
        )
        
        # Extrae y devuelve la respuesta generada
        return {"recommendation": chat_completion.choices[0].message["content"]}
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
        description="This service generates recommendations using OpenAI.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.on_event("startup")
async def startup_event():
    openapi_schema = custom_openapi()
    # Asegúrate de que el directorio 'static' exista en tu proyecto
    with open('static/openapi.json', 'w') as file:
        json.dump(openapi_schema, file)

app.openapi = custom_openapi

# Monta el directorio 'static' para servir el esquema OpenAPI generado
app.mount("/static", StaticFiles(directory="static"), name="static")
