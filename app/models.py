from pydantic import BaseModel

class Meal(BaseModel):
    main_dish : str = ""
    drink: str = ""
    dessert: str = ""

class RecommendationRequest(BaseModel):
    meal : Meal
    recommendation_of : list[str]
    src : str
