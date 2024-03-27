from src.database.database_setup import DatabaseSetup
from src.recommendations.collaborative_filtering import ProductRecommender
import sys


def main():
    # Setup database connection
    db_uri = "bolt://localhost:7687"
    db_user = "neo4j"
    db_password = "password"

    # Initialize database setup
    db_setup = DatabaseSetup(db_uri, db_user, db_password)
    # You can add database setup related calls here if needed
    db_setup.create_constraints()

    # Initialize recommendation modules
    collaborative_filter = ProductRecommender(db_uri, db_user, db_password)

    # User input (for demonstration purposes, replace with actual user ID)
    user_id = input("Enter User ID for recommendations: ")

    # Get recommendations
    print("User-Based Collaborative Recommendations:")
    print(collaborative_filter.get_user_based_recommendations(user_id))

    print("Category-Based Collaborative Recommendations:")
    print(collaborative_filter.get_category_based_recommendations(user_id))

    # Close database connection
    db_setup.close()
    collaborative_filter.close()


if __name__ == "__main__":
    main()
