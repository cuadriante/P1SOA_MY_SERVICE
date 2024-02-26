from pydantic import BaseModel

class Meal(BaseModel):
    main_dish : str = ""
    drink: str = ""
    dessert: str = ""