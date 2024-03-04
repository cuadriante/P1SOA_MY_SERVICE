from pydantic import BaseModel
from enum import Enum
from typing import List

# Define an Enum to specify the allowed recommendation types
class RecommendationType(str, Enum):
    main_dish = "main_dish"
    drink = "drink"
    dessert = "dessert"

# Define an Enum to specify the allowed sources
class SourceType(str, Enum):
    openai = "openai"
    localdb = "localdb"
    external = "external"
    
    
class Meal(BaseModel):
    main_dish : str = ""
    drink: str = ""
    dessert: str = ""

class RecommendationRequest(BaseModel):
    meal : Meal
    recommendation_of : List[RecommendationType]
    src : SourceType


class externalObject:
    def __init__(self,meal,drink,dessert):
        self.meal=meal
        self.drink=drink
        self.dessert=dessert

