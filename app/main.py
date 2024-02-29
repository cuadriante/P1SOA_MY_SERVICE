
from routes import recommendation
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field 
from app.data.JsonDataCollector import JsonDataCollector
from app.DefaultRecommender.DefaultRecommender import *
import openai
import os
from dotenv import load_dotenv
from starlette.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
import json

app = FastAPI()
app.include_router(recommendation.router)
# Load environment variables from .env file in the current directory
load_dotenv()

app = FastAPI()

# Configure OpenAI client with API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class RecommendationRequest(BaseModel):
    input: str = Field(..., example="main dish")
    recommendation_of: list = Field(..., example=["dessert"])
    recommendation_type: str = Field(..., example="default")

json_data_collector = JsonDataCollector()
default_recommender = DefaultRecommender(json_data_collector)

@app.post("/generate-recommendation/")
async def generate_recommendation(request: RecommendationRequest):
    try:
        if request.recommendation_type == "default":
            response_content = default_recommender.recommend(
                request.input, 
                request.input_type, 
                request.recommendation_of)
        elif request.recommendation_type == "ai_generated":
            response_content = generate_ai_response(request)
        elif request.recommendation_type == "dynamic":
            response_content = get_dynamic_response(request.external_api_details)
        else:
            raise HTTPException(status_code=400, detail="Invalid recommendation type")

        return {"recommendation": response_content}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except FileNotFoundError as fnfe:
        raise HTTPException(status_code=404, detail=str(fnfe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def generate_ai_response(request: RecommendationRequest):
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": request.input,
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
        title="Recommendation Service API",
        version="1.0.0",
        description="This service generates recommendations using OpenAI, Predefined Data or External APIs.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.on_event("startup")
async def startup_event():
    openapi_schema = custom_openapi()
    # Asegúrate de que el directorio 'static' exista en tu proyecto
    with open('../static/openapi.json', 'w') as file:
        json.dump(openapi_schema, file)

app.openapi = custom_openapi
# Monta el directorio 'static' para servir el esquema OpenAPI generado
#app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
