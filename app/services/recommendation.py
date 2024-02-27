from fastapi import HTTPException
from .database import get_predefined_suggestion
from .openAIapi import get_OpenAI_suggestion

def process_recommendation_req(entry: str, src: str) -> str:
    # Validar el contenido del request
    validate_request_src(src)
    if src.upper() == "OPENAI":
        response = get_OpenAI_suggestion(entry)
    elif src.upper() == "LOCALDB":
        response = get_predefined_suggestion(entry)
    elif src.upper() == "EXTERNAL":
        response = "WIP"
    return response
        
        
def validate_request_src(req_source):
    if req_source is None:
        raise HTTPException(status_code=400, detail="The source was not supplied") 
    if req_source.upper() not in ["OPENAI", "LOCALDB", "EXTERNAL"]:
        raise HTTPException(status_code=400, detail="The introduced source is not found") 