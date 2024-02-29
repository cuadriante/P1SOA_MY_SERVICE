import unittest
from models import Meal
from services.database import JsonDataSource

json_data = [
    {
        "main_dish": "pizza",
        "drink": "coke",
        "dessert": "ice cream"
    },
    {
        "main_dish":"salad",
        "drink":"smoothie",
        "dessert":"watermelon"
    },
    {
        "main_dish":"sandwich",
        "drink":"water",
        "dessert":"cake"
    }

]


class TestJsonDataSource(unittest.TestCase):
    def test_get_meal_expected_success(self):
        data_collector = JsonDataSource()
        data_collector.meals = json_data
        input = "pizza"

        result = data_collector.get_meal(input)

        meal = Meal(main_dish="pizza", drink="coke", dessert="ice cream")
        self.assertEqual(result, meal)

    def test_get_input_not_found_expected_none(self):
        data_collector = JsonDataSource()
        data_collector.meals = json_data
        input = "juanilama"

        result = data_collector.get_meal(input)

        self.assertEqual(result, Meal())
