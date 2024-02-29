from fastapi import HTTPException
from .predefined_recom import init_default_recommender
from .database import init_data_source
from .openAIapi import get_OpenAI_suggestion


data_source = init_data_source()
predefined_recommender = init_default_recommender(data_source)


def process_recommendation_req(entry: str, recomendation_of: list[str] , src: str) -> str:
    # Validar el contenido del request
    validate_request_src(src)
    if src.upper() == "OPENAI":
        response = get_OpenAI_suggestion(entry, recomendation_of)
    elif src.upper() == "LOCALDB":
        response = process_predefined_recom(entry, recomendation_of, src)
    elif src.upper() == "EXTERNAL":
        response = "WIP"
    return response

def process_predefined_recom(entry: str, recomendation_of: list[str]) -> str:
    try:
        response = predefined_recommender.recommend(entry, recomendation_of)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args) from e
        
        
def validate_request_src(req_source):
    if req_source is None:
        raise HTTPException(status_code=400, detail="The source was not supplied") 
    if req_source.upper() not in ["OPENAI", "LOCALDB", "EXTERNAL"]:
        raise HTTPException(status_code=400, detail="The introduced source is not found") 