# Usage Guide for Product Recommendation System

## Overview
This document describes how to use the product recommendation system.

### Starting the System
Ensure Neo4j is running and accessible. Execute `recommendation_system.py` to start the system.

### Getting Recommendations
1. **User-Based Recommendations**:
   Retrieve products recommended based on user similarity.
   ```python
   recommender.get_user_based_recommendations(user_id)

2. **Item-Based Recommendations**:
Get products often bought together with those the user has purchased.
    ```python
   recommender.get_item_based_recommendations(user_id)

3. **Category-Based Recommendations**:
Suggestions based on the user's favorite product category.
    ```python
   recommender.get_category_based_recommendations(user_id)
