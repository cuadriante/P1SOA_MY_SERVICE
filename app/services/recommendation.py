from fastapi import HTTPException
# from .database import get_predefined_suggestion
from .predefined_recom import PredefinedRecommender
from .database import JsonDataSource
from .openAIapi import get_OpenAI_suggestion

JSON_DATA_PATH = '../data/predefined_recom.json'
json_data_source = JsonDataSource(JSON_DATA_PATH)
predefined_recommender = PredefinedRecommender(json_data_source)


def process_recommendation_req(entry: str, recomendation_of: list[str] , src: str) -> str:
    # Validar el contenido del request
    validate_request_src(src)
    if src.upper() == "OPENAI":
        response = get_OpenAI_suggestion(entry, recomendation_of)
    elif src.upper() == "LOCALDB":
        response = predefined_recommender.recommend(entry, recomendation_of)
    elif src.upper() == "EXTERNAL":
        response = "WIP"
    return response
        
        
def validate_request_src(req_source):
    if req_source is None:
        raise HTTPException(status_code=400, detail="The source was not supplied") 
    if req_source.upper() not in ["OPENAI", "LOCALDB", "EXTERNAL"]:
        raise HTTPException(status_code=400, detail="The introduced source is not found") 