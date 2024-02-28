from models import Meal

from abc import ABC, abstractmethod
import json

# json_data_path = 'data/predefined_recom.json'

class IDataSource(ABC):
    @abstractmethod
    def get_meal(self, input: str) -> None:
        pass

class JsonDataSource(IDataSource):
    def __init__(self, datafile_path=None):
        self.meals = []
        if datafile_path:
            self.__load_data(datafile_path)

    def __load_data(self, datafile_path):
        self.meals = json.load(open(datafile_path))


    def get_meal(self, input : str):
        for meal in self.meals:
            for food_type, food in meal.items():
                if input.lower() == food.lower():
                    return self.__dict_to_meal(meal)
        return Meal()
            
    def __dict_to_meal(self, meal_dict):
        return Meal(**meal_dict)