import requests
from models import Meal
from models import externalObject
from fastapi import HTTPException

URL_external_service="http://soa41d-project1.eastus.azurecontainer.io/recommendation/custom"

def get_external_recom(meal: Meal, recomendation_of: list[str]) -> str:
    try:
        recomendation_of=recomendation_of+ get_non_empty_fields(meal)
        request_params_dict=map_internal_to_external(meal)
        external_response=requests.get(URL_external_service,params=request_params_dict)
        response_dict_external=external_response.json()
        return map_external_to_internal(response_dict_external,recomendation_of)
    except:
        try:
            raise HTTPException(status_code=external_response.status_code, detail=external_response.reason) 
        except:
            raise HTTPException(status_code=503, detail="Service Unavailable") 
            

def class_to_dict(obj):
    return {key: value for key, value in vars(obj).items() if value}


def filter_dict_by_keys(input_dict, key_list):
    return {key: value for key, value in input_dict.items() if key in key_list}

def get_non_empty_fields(obj):
    return [attr for attr, value in vars(obj).items() if value]

def map_internal_to_external(internal):
    request_params= externalObject(internal.main_dish,internal.drink,internal.dessert)
    request_params_dict=class_to_dict(request_params)
    return request_params_dict
def map_external_to_internal(external,requested_values):
    response_dict_internal={
        "main_dish": external["meal"],
        "drink": external["drink"],
        "dessert": external["dessert"]  
    }
    response_final_dict=filter_dict_by_keys(response_dict_internal,requested_values)
    print(response_final_dict)
    return Meal(**response_final_dict)
    
