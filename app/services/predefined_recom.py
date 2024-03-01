import random
from models import Meal
from .database import IDataSource


def init_default_recommender(data_source: IDataSource):
    return PredefinedRecommender(data_source)

class PredefinedRecommender:
    def __init__(self, data_source: IDataSource):
        self.data_source = data_source


    def recommend(self, input, recommendation_of):
        posible_food_by_type = self.get_posible_meals(input)
        # self.check_if_enough(posible_food_by_type)
        recommendation = {}
        for item in recommendation_of:
            if item == "main_dish":
                recommendation["main_dish"] = random.choice(posible_food_by_type["main_dish"])
            elif item == "drink":
                recommendation["drink"] = random.choice(posible_food_by_type["drink"])
            elif item == "dessert":
                recommendation["dessert"] = random.choice(posible_food_by_type["dessert"])
            else:
                raise TypeError("Invalid recommendation type: " + item)
        return recommendation
    
    # def check_if_enough(self, posible_food_by_type):
    #     if len(posible_food_by_type["main_dish"]) == 0:
    #         raise ValueError("There are no recommendations available for your input. Please try another one.")
    
    def get_posible_meals(self, user_food):
        user_food = self.make_input_a_list(user_food)
        posible_meals = []
        for food in user_food:
            meal = self.data_source.get_meal(food)
            posible_meals.append(meal)
        return self.refactor_meals(posible_meals)
    
    def refactor_meals(self, posible_meals):
        posible_meals = self.remove_empty_meals(posible_meals)
        meal_by_type = self.rearange_food_by_type(posible_meals)
        return meal_by_type
    
    def make_input_a_list(self, input):
        if isinstance(input, list):
            return input
        else:
            return [input]
        
    def remove_empty_meals(self, posible_meals):
        return [meal for meal in posible_meals if meal.main_dish != ""]
    
    def rearange_food_by_type(self, posible_meals):
        recommendation_pool = {}
        recommendation_pool["main_dish"] = []
        recommendation_pool["drink"] = []
        recommendation_pool["dessert"] = []
        for meal in posible_meals:
            recommendation_pool["main_dish"].append(meal.main_dish)
            recommendation_pool["drink"].append(meal.drink)
            recommendation_pool["dessert"].append(meal.dessert)
        return recommendation_pool
    
