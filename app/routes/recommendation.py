from fastapi import APIRouter, HTTPException
from models import RecommendationRequest, Meal
from services.recommendation import process_recommendation_req

router = APIRouter()

@router.post("/gen-recommendation/",     responses={
        400: {"description": "<br>Bad Request: The source was not supplied or the introduced source is not found. <br>" 
                                              "The introduced source is not found"}}, 
        response_model=Meal)
async def generate_recommendation(request: RecommendationRequest):
    try:
        response = process_recommendation_req(request.meal, request.recommendation_of, request.src)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))