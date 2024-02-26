import unittest
import Recommender as rc

class TestDefaultRecommender(unittest.TestCase):

    def test_recommend_input_main_dish_expected_drink_and_dessert(self):
        input = "pizza"
        input_type = "main_dish"
        recommendation_of = ["drink", "dessert"]
        default_recommender = rc.DefaultRecommender()

        result = default_recommender.recommend(input, input_type, recommendation_of)

        self.assertEqual(result, {"drink": "coke", "dessert": "ice cream"})

    def test_recommend_input_drink_expected_dessert(self):
        input = "water"
        input_type = "drink"
        recommendation_of = ["dessert"]
        default_recommender = rc.DefaultRecommender()

        result = default_recommender.recommend(input, input_type, recommendation_of)

        self.assertEqual(result, {"dessert": "cake"})
        
    def test_recommend_input_dessert_expected_main_dish_and_dessert(self):
        input = "watermelon"
        input_type = "dessert"
        recommendation_of = ["main_dish", "drink"]
        default_recommender = rc.DefaultRecommender()

        result = default_recommender.recommend(input, input_type, recommendation_of)

        self.assertEqual(result, {"main_dish": "salad", "drink": "smoothie"})

    def test_recommend_input_not_fount_expected_empty_return(self):
        input = "juanilama"
        input_type = "main_dish"
        recommendation_of = ["dessert", "drink"]
        default_recommender = rc.DefaultRecommender()

        result = default_recommender.recommend(input, input_type, recommendation_of)

        self.assertEqual(result, {"dessert": "", "drink": ""})

    def test_recommend_invalid_input_type_expected_error(self):
        input = "pizza"
        input_type = "entree"
        recommendation_of = ["drink", "dessert"]
        default_recommender = rc.DefaultRecommender()

        with self.assertRaises(TypeError) as context: 
            default_recommender.recommend(input, input_type, recommendation_of)

        self.assertEqual(str(context.exception), "Invalid input type: " + input_type)

    def test_recommend_invalid_recommentaion_of_expected_error(self):
        input = "pizza"
        input_type = "main_dish"
        recommendation_of = ["entree"]
        default_recommender = rc.DefaultRecommender()

        with self.assertRaises(TypeError) as context: 
            default_recommender.recommend(input, input_type, recommendation_of)

        self.assertEqual(str(context.exception), "Invalid recommendation type: " + recommendation_of[0])

# if __name__ == '__main__': #runs test if this file is run as main
#     unittest.main()
