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
    recommendation_type: str
    external_api_details: str = None

@app.post("/generate-recommendation/")
async def generate_recommendation(request: RecommendationRequest):
    try:
        if request.recommendation_type == "predetermined":
            response_content = "Respuesta predeterminada basada en la categoría."
        elif request.recommendation_type == "ai_generated":
            response_content = generate_ai_response(request)
        elif request.recommendation_type == "dynamic":
            response_content = get_dynamic_response(request.external_api_details)
        else:
            raise HTTPException(status_code=400, detail="Tipo de recomendación no válido")

        return {"recommendation": response_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def generate_ai_response(request: RecommendationRequest):
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
                    "content": "You are an intelligent assistant that gives main course, drink and dessert recommendations that go with the user inputed food, drink or general request. if a request is out of this scope, you answer with an apology.",
                },
            ],
        )
        
        response = chat_completion.choices[0].message.content
        return response
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

def get_dynamic_response(api_details: str):
    # Esta función debería implementarse para realizar solicitudes a APIs externas
    # y procesar la respuesta para devolver una recomendación.
    # Ejemplo de implementación pendiente.
    return "Respuesta dinámica basada en API externa."

# Monta el directorio 'static' para servir el esquema OpenAPI generado
app.mount("/static", StaticFiles(directory="static"), name="static")
