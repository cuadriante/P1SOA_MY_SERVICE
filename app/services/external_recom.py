from models import Meal
from models import ExternalRequest
URL_external_service=""
def get_external_recom(meal: Meal, recomendation_of: list[str]) -> str:
    body_request= ExternalRequest()
    external_response=requests.post(URL_external_service,json=body_request)
    return external_response
    
