from fastapi import FastAPI
from routes import recommendation

from starlette.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
import json

app = FastAPI()
app.include_router(recommendation.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the recommendation service"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom Recommendation Service",
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