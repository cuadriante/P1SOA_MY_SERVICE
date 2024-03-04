from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

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
    main_dish: Optional[str] = Field(default=None, example="Pasta")
    drink: Optional[str] = Field(default=None, example="")
    dessert: Optional[str] = Field(default=None, example="")

class RecommendationRequest(BaseModel):
    meal : Meal = Field(..., example={
        "main_dish": "Pasta",
        "drink": "",
        "dessert": ""
    })
    recommendation_of : List[RecommendationType] = Field(..., example=["drink", "dessert"])
    src : SourceType = Field(..., example="openai")
