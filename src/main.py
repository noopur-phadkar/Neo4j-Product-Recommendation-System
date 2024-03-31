from src.database.database_setup import DatabaseSetup
from src.recommendations.collaborative_filtering import ProductRecommender


def main():

    # Initialize database setup
    db_setup = DatabaseSetup()
    # You can add database setup related calls here if needed
    db_setup.create_constraints()

    # Initialize recommendation modules
    collaborative_filter = ProductRecommender(db_setup.driver)

    # User input (for demonstration purposes, replace with actual user ID)
    user_id = input("Enter User ID for recommendations: ")

    # Get recommendations
    print("User-Based Collaborative Recommendations:")
    print(collaborative_filter.get_user_based_recommendations(user_id))

    print("Category-Based Collaborative Recommendations:")
    print(collaborative_filter.get_category_based_recommendations(user_id))

    # Close database connection
    db_setup.close()


if __name__ == "__main__":
    main()
