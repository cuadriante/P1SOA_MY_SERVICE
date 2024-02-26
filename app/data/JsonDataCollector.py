import json
from app.Meal import Meal
from app.data.IDataCollector import IDataCollector
DATAFILE_PATH = "app/data/meals.json"

class JsonDataCollector(IDataCollector):
    def __init__(self, datafile_path=DATAFILE_PATH):
        self.meals = []
        if datafile_path:
            self.__load_data(datafile_path)

    def __load_data(self, datafile_path):
        self.meals = json.load(open(datafile_path))

    def get_meal(self, input, input_type):
        if self.__check_for_input_type(input_type):
            return self.__collect_meal(input, input_type)
        else:
            raise TypeError("Invalid input type: " + input_type)

    def __check_for_input_type(self, input_type):
        return input_type in self.meals[0]

    def __collect_meal(self, input, input_type):
        for meal in self.meals:
            if meal.get(input_type) == input:
                return self.__dict_to_meal(meal)
        return Meal()
            
    def __dict_to_meal(self, meal_dict):
        return Meal(**meal_dict)

