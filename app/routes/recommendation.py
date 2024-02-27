from fastapi import APIRouter, HTTPException
from models import RecommendationRequest
from services.recommendation import process_recommendation_req

router = APIRouter()

@router.post("/gen-recommendation/")
async def generate_recommendation(request: RecommendationRequest):
    try:
        response = process_recommendation_req(request.description, request.src)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))