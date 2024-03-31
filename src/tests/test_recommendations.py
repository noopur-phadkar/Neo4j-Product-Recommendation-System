import unittest
from src.database.database_setup import DatabaseSetup
from src.recommendations.collaborative_filtering import ProductRecommender


class TestRecommendations(unittest.TestCase):

    def test_recommendations(self):
        # Initialize database setup
        db_setup = DatabaseSetup()
        # You can add database setup related calls here if needed
        db_setup.create_constraints()

        recommender = ProductRecommender(db_setup.driver)
        user_id = "1"  # Replace with the actual target user ID

        print("User-Based Recommendations:", recommender.get_user_based_recommendations(user_id))
        print("Category-Based Recommendations:", recommender.get_category_based_recommendations(user_id))