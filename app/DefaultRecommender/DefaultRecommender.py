from app.Meal import Meal
from app.data.IDataCollector import IDataCollector

class DefaultRecommender:
    def __init__(self, data_collector: IDataCollector):
        self.data_collector = data_collector

    def recommend(self, input, input_type, recommendation_of):
        meal = self.data_collector.get_meal(input, input_type)
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

