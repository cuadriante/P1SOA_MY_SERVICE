from models import Meal
from .database import IDataSource

class PredefinedRecommender:
    def __init__(self, data_source: IDataSource):
        self.data_source = data_source

    def recommend(self, input, recommendation_of):
        meal = self.data_source.get_meal(input)
        recommendation = {}
        for item in recommendation_of:
            if item == "main_dish":
                recommendation["main_dish"] = meal.main_dish
            elif item == "drink":
                recommendation["drink"] = meal.drink 
            elif item == "dessert":
                recommendation["dessert"] = meal.dessert
            else:
                raise TypeError("Invalid recommendation type: " + item)
        return recommendation