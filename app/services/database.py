from models import Meal

from abc import ABC, abstractmethod
import json

JSON_DATA_PATH = '../data/predefined_recom.json'

def init_data_source():
    return JsonDataSource(JSON_DATA_PATH)

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
        
    def get_meal(self, input_food : str):
        for meal in self.meals:
            for food_type, db_food in meal.items():
                if input_food.lower() == db_food.lower():
                    return meal
        return Meal().__dict__
            