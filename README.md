# Product-Recommender-System
This is a Real-Time Product Recommender System with Graph Databases: Leveraging Neo4j and BigQuery for E-commerce Data Analysis


## Recommendation Systems

Recommendation systems help customers find products they are interested in and increase the likelihood of making a purchase.

The two primary types of recommender systems
- **Content-based systems** focuses on the similarities between products. For instance, products that belong in the same category as those previously purchased by the user are recommended. 
- **Collaborative systems** examines the interactions between the users and the store such that the target user is recommended products based on other users who share similar habits and preferences.

## Why use graph database for recommendation systems?

A graph database is highly beneficial for a recommender system due to its ability to efficiently handle complex and interconnected data. 

In such databases, data is stored as nodes and edges, representing entities and their relationships. This structure is inherently suitable for recommender systems, which rely heavily on relationship analysis and pattern recognition. 

Graph databases excel in identifying connections and patterns among large datasets, enabling more accurate and personalized recommendations based on user preferences, behavior, and network relationships. This leads to a more intuitive and relevant user experience in recommendation scenarios.

For this project I am using - Neo4j

## Dataset

The project utilizes the Google merchandise store dataset, available through BigQuery. This dataset encompasses a range of e-commerce information, including:

- **Visitor Session Data**: Details of store visitors' sessions, capturing user interactions.
- **Product Information**: Data on various products, including prices and categories, providing insights into product diversity.
- **User-Product Interactions**: Relationships between users and products, like session durations on specific product pages, offering a nuanced view of user engagement.

This rich dataset forms the backbone of the product recommendation system, enabling detailed analysis and modeling of user behavior and product preferences.