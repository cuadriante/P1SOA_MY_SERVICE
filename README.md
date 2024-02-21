# P1SOA_MY_SERVICE
Servicio web capaz de comunicarse con servicios externos

Para correr FastAPI: 
uvicorn main:app --reload

para probar recomendaciones de tipo ai_generated:

http://localhost:8000/docs#/default/generate_recommendation_generate_recommendation__post

{
  "description": "a romantic dinner",
  "recommendation_type": "ai_generated",
  "external_api_details": "string"
}
