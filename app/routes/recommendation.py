from fastapi import APIRouter, HTTPException
from models import RecommendationRequest, Meal
from services.recommendation import process_recommendation_req

router = APIRouter()

@router.post("/gen-recommendation/",     responses={
        200: {
                "description": "Successful Response",
                "content": {
                    "application/json": {
                        "example": {"main_dish": "Pizza", "drink": "Soda", "dessert": "Cake"}
                }
                }
            },
            400: {
                "description": "Bad Request: The source was not supplied or the introduced source is not found.",
                "content": {
                    "application/json": {
                        "example": {"detail": "The source was not supplied or the introduced source is not found."}
                    }
                }
            },
            502: {
                "description": "Bad Gateway: Problem with the upstream server (OpenAI).",
                "content": {
                    "application/json": {
                        "example": {"detail": "OpenAI service encountered an issue, please try again."}
                    }
                }
                }
        }, 
        response_model=RecommendationRequest)
async def generate_recommendation(request: RecommendationRequest):
    try:
        response = process_recommendation_req(request.meal, request.recommendation_of, request.src)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))