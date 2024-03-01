import unittest
from unittest.mock import MagicMock
from models import Meal
from services.database import JsonDataSource
from services.predefined_recom import PredefinedRecommender

class TestDefaultRecommender(unittest.TestCase):

    def test_rearenge_food_by_type_expected_dict(self):
        meals = [Meal(main_dish="pizza", drink="coke", dessert="ice cream"), Meal(main_dish="salad", drink="water", dessert="cake")]
        mock_data_source = JsonDataSource()
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.rearange_food_by_type(meals)

        self.assertEqual(result, {"main_dish": ["pizza", "salad"], "drink": ["coke", "water"], "dessert": ["ice cream", "cake"]})

    def test_remove_empty_meals_expected_list(self):
        meals = [Meal(main_dish="pizza", drink="coke", dessert="ice cream"), Meal()]
        mock_data_source = JsonDataSource()
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.remove_empty_meals(meals)

        self.assertEqual(result, [Meal(main_dish="pizza", drink="coke", dessert="ice cream")])

    def test_refactor_meals_expected_dict(self):
        meals = [Meal(main_dish="pizza", drink="coke", dessert="ice cream"), Meal(main_dish="salad", drink="water", dessert="cake"), Meal()]
        mock_data_source = JsonDataSource()
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.refactor_meals(meals)

        self.assertEqual(result, {"main_dish": ["pizza", "salad"], "drink": ["coke", "water"], "dessert": ["ice cream", "cake"]})

    def test_get_posible_meals_expected_one_meal(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock(return_value=Meal(main_dish="pizza", drink="coke", dessert="ice cream"))
        input = "pizza"
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.get_posible_meals(input)

        mock_data_source.get_meal.assert_called_once_with(input)
        self.assertEqual(result, {"main_dish": ["pizza"], "drink": ["coke"], "dessert": ["ice cream"]})

    def test_get_posible_meals_expected_two_meals(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock()
        mock_data_source.get_meal.side_effect = [
            Meal(main_dish="pizza", drink="coke", dessert="ice cream"),
            Meal(main_dish="pasta", drink="wine", dessert="tiramisu")]
        input = ["pizza", "wine"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.get_posible_meals(input)

        # mock_data_source.get_meal.assert_called_once_with("pizza")
        self.assertEqual(result, {"main_dish": ["pizza", "pasta"], "drink": ["coke", "wine"], "dessert": ["ice cream", "tiramisu"]})


    def test_recommend_input_main_dish_expected_drink_and_dessert(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock(return_value=Meal(main_dish="pizza", drink="coke", dessert="ice cream"))
        input = "pizza"
        recommendation_of = ["drink", "dessert"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.recommend(input,recommendation_of)
        
        mock_data_source.get_meal.assert_called_once_with(input)
        self.assertEqual(result, {"drink": "coke", "dessert": "ice cream"})


    def test_recommend_input_drink_expected_dessert(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock(return_value=Meal(main_dish="sandwich", drink="water", dessert="cake"))
        input = "water"
        recommendation_of = ["dessert"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.recommend(input, recommendation_of)

        mock_data_source.get_meal.assert_called_once_with(input)
        self.assertEqual(result, {"dessert": "cake"})

        
    def test_recommend_input_dessert_expected_main_dish_and_dessert(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock(return_value=Meal(main_dish="salad", drink="smoothie", dessert="watermelon"))
        input = "watermelon"
        recommendation_of = ["main_dish", "drink"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.recommend(input, recommendation_of)

        mock_data_source.get_meal.assert_called_once_with(input)
        self.assertEqual(result, {"main_dish": "salad", "drink": "smoothie"})

    # def test_recommend_input_not_fount_expected_value_error(self):
    #     mock_data_source = JsonDataSource()
    #     mock_data_source.get_meal = MagicMock(return_value=Meal())
    #     input = "juanilama"
    #     recommendation_of = ["dessert", "drink"]
    #     default_recommender = PredefinedRecommender(mock_data_source)

    #     with self.assertRaises(ValueError) as context: 
    #         default_recommender.recommend(input, recommendation_of)
    #     self.assertEqual(str(context.exception), "There are no recommendations available for your input. Please try another one.")

    def test_recommend_invalid_recommentaion_of_expected_error(self):
        mock_data_source = JsonDataSource()
        MagicMock(return_value=Meal(main_dish="pizza", drink="coke", dessert="ice cream"))
        input = "pizza"
        recommendation_of = ["entree"]
        default_recommender = PredefinedRecommender(mock_data_source)

        with self.assertRaises(TypeError) as context: 
            default_recommender.recommend(input, recommendation_of)
        self.assertEqual(str(context.exception), "Invalid recommendation type: " + recommendation_of[0])
