import unittest
from unittest.mock import MagicMock
from models import Meal
from services.database import JsonDataSource
from services.predefined_recom import PredefinedRecommender

class TestDefaultRecommender(unittest.TestCase):

    def test_remove_empty_meals_expected_list(self):
        meals = {"main_dish": ["pizza", ""], "drink":["coke",""], "dessert":["ice cream", ""]}
        mock_data_source = JsonDataSource()
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.remove_empty_meals(meals)

        self.assertEqual(result, {"main_dish": ["pizza"], "drink":["coke"], "dessert":["ice cream"]})


    def test_get_candidate_food_by_type_expected_two_meals(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock()
        mock_data_source.get_meal.side_effect = [
            {"main_dish":"pizza", "drink":"coke", "dessert":"ice cream"},
            {"main_dish":"pasta", "drink":"wine", "dessert":"tiramisu"},
            {"main_dish":"", "drink":"", "dessert":""},
        ]
        user_meal = {"main_dish":"pizza", "drink":"coke", "dessert":""}
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.get_candidate_food_by_type(user_meal)

        self.assertEqual(result, {"main_dish": ["pizza", "pasta"], "drink": ["coke", "wine"], "dessert": ["ice cream", "tiramisu"]})


    def test_recommend_input_main_dish_expected_drink_and_dessert(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock(return_value={"main_dish":"pizza", "drink":"coke", "dessert":"ice cream"})
        user_meal = (Meal(main_dish="pizza", drink="", dessert=""))
        recommendation_of = ["drink", "dessert"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.recommend(user_meal,recommendation_of)
        
        self.assertEqual(result, Meal(main_dish="pizza", drink="coke", dessert="ice cream"))

    def test_recommend_input_drink_expected_dessert(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock()
        mock_data_source.get_meal.side_effect = [
            {"main_dish":"sandwich", "drink":"water", "dessert":"cake"},
            {"main_dish":"", "drink":"", "dessert":""},
            {"main_dish":"", "drink":"", "dessert":""},
        ]
        user_meal = (Meal(main_dish="", drink="water", dessert=""))
        recommendation_of = ["dessert"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.recommend(user_meal, recommendation_of)

        self.assertEqual(result, Meal(main_dish="", drink="water", dessert="cake"))

        
    def test_recommend_input_dessert_expected_main_dish_and_dessert(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock()
        mock_data_source.get_meal.side_effect = [
            {"main_dish":"salad", "drink":"smoothie", "dessert":"watermelon"},
            {"main_dish":"", "drink":"", "dessert":""},
            {"main_dish":"", "drink":"", "dessert":""}
        ]
        user_input = (Meal(main_dish="", drink="", dessert="watermelon"))
        recommendation_of = ["main_dish", "drink"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.recommend(user_input, recommendation_of)

        self.assertEqual(result, Meal(main_dish="salad", drink="smoothie", dessert="watermelon"))


    def test_recommend_invalid_recommentaion_of_expected_error(self):
        mock_data_source = JsonDataSource()
        MagicMock({"main_dish":"pizza", "drink":"coke", "dessert":"ice cream"})
        user_meal = (Meal(main_dish="pizza", drink="", dessert=""))
        recommendation_of = ["entree"]
        default_recommender = PredefinedRecommender(mock_data_source)

        with self.assertRaises(TypeError) as context: 
            default_recommender.recommend(user_meal, recommendation_of)
        self.assertEqual(str(context.exception), "Invalid recommendation type: " + recommendation_of[0])

    def test_recommend_input_not_fount_expected_error(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock(return_value=Meal())
        user_meal = (Meal(main_dish="juanilama", drink="", dessert=""))
        recommendation_of = ["dessert", "drink"]
        default_recommender = PredefinedRecommender(mock_data_source)

        with self.assertRaises(TypeError) as context: 
            default_recommender.recommend(user_meal, recommendation_of)
        self.assertEqual(str(context.exception), "There are no recommendations available for your input. Please try another one.")