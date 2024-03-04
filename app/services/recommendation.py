from fastapi import HTTPException

from models import Meal
from .predefined_recom import get_predefined_recom
from .openAIapi import get_OpenAI_suggestion
from .external_recom import get_external_recom


def process_recommendation_req(meal: Meal, recomendation_of: list[str] , src: str) -> str:
    # Validar el contenido del request
    validate_request_src(src)
    if src.upper() == "OPENAI":
        response = get_OpenAI_suggestion(meal, recomendation_of)
    elif src.upper() == "LOCALDB":
        response = get_predefined_recom(meal, recomendation_of)
    elif src.upper() == "EXTERNAL":
        response = get_external_recom(meal,recomendation_of)
    return response
        
def validate_request_src(req_source):
    if req_source is None or req_source == "":
        raise HTTPException(status_code=400, detail="The source was not supplied") 
    if req_source.upper() not in ["OPENAI", "LOCALDB", "EXTERNAL"]:
        raise HTTPException(status_code=400, detail="The introduced source is not found") 
    
def validate_meal(meal):
    if not meal or not isinstance(meal, Meal):
        raise HTTPException(status_code=400, detail="Invalid meal data provided")

def validate_recommendation_of(recommendation_of):
    if not recommendation_of or not isinstance(recommendation_of, list) or not all(isinstance(item, str) for item in recommendation_of):
        raise HTTPException(status_code=400, detail="Invalid recommendation_of data provided")