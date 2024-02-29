import unittest
from unittest.mock import MagicMock
from models import Meal
from services.database import JsonDataSource
from services.predefined_recom import PredefinedRecommender

class TestDefaultRecommender(unittest.TestCase):

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

    def test_recommend_input_not_fount_expected_empty_return(self):
        mock_data_source = JsonDataSource()
        mock_data_source.get_meal = MagicMock(return_value=Meal())
        input = "juanilama"
        recommendation_of = ["dessert", "drink"]
        default_recommender = PredefinedRecommender(mock_data_source)

        result = default_recommender.recommend(input, recommendation_of)

        self.assertEqual(result, {"dessert": "", "drink": ""})

    def test_recommend_invalid_recommentaion_of_expected_error(self):
        mock_data_source = JsonDataSource()
        MagicMock(return_value=Meal(main_dish="pizza", drink="coke", dessert="ice cream"))
        input = "pizza"
        recommendation_of = ["entree"]
        default_recommender = PredefinedRecommender(mock_data_source)

        with self.assertRaises(TypeError) as context: 
            default_recommender.recommend(input, recommendation_of)
        self.assertEqual(str(context.exception), "Invalid recommendation type: " + recommendation_of[0])
