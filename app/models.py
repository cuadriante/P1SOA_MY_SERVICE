from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    input : list[str]
    recommendation_of : list[str]
    src : str

class Meal(BaseModel):
    main_dish : str = ""
    drink: str = ""
    dessert: str = ""