import unittest
from app.Meal import Meal
from app.data.JsonDataCollector import *

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


class TestDataCollector(unittest.TestCase):
    def test_get_meal_expected_success(self):
        data_collector = JsonDataCollector()
        data_collector.meals = json_data
        input = "pizza"
        input_type = "main_dish"

        result = data_collector.get_meal(input, input_type)

        meal = Meal(main_dish="pizza", drink="coke", dessert="ice cream")
        self.assertEqual(result, meal)

    def test_get_input_not_found_expected_none(self):
        data_collector = JsonDataCollector()
        data_collector.meals = json_data
        input = "juanilama"
        input_type = "main_dish"

        result = data_collector.get_meal(input, input_type)

        self.assertEqual(result, Meal())

    def test_get_meal_invalid_input_type_expected_error(self):
        data_collector = JsonDataCollector()
        data_collector.meals = json_data
        input = "pizza"
        input_type = "entree"

        with self.assertRaises(TypeError) as context:
            data_collector.get_meal(input, input_type)

        self.assertEqual(str(context.exception), "Invalid input type: " + input_type)
