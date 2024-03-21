<!--
## Dataset

The project utilizes the Google merchandise store dataset, available through BigQuery. This dataset encompasses a range of e-commerce information, including:

- **Visitor Session Data**: Details of store visitors' sessions, capturing user interactions.
- **Product Information**: Data on various products, including prices and categories, providing insights into product diversity.
- **User-Product Interactions**: Relationships between users and products, like session durations on specific product pages, offering a nuanced view of user engagement.

This rich dataset forms the backbone of the product recommendation system, enabling detailed analysis and modeling of user behavior and product preferences.
-->
# Real-Time Product Recommendation System

## Overview
This system is a real-time product recommendation engine using Neo4j. It's designed to provide personalized product suggestions to users based on their behavior and preferences.

### Key Features
- User-Based Collaborative Filtering
- Item-Based Collaborative Filtering
- Category-Based Recommendations

### Data Sources
- Initially utilizes data from [Fake Store API](https://fakestoreapi.com) for development and testing.
- Final implementation will leverage data from Google's BigQuery.

## Recommendation Systems

Recommendation systems help customers find products they are interested in and increase the likelihood of making a purchase.

The two primary types of recommender systems
- **Content-based systems** focus on the similarities between products. For instance, products in the same category as those previously purchased by the user are recommended. 
- **Collaborative systems** examine the interactions between the users and the store such that the target user is recommended products based on other users who share similar habits and preferences.

## Why use graph databases for recommendation systems?

A graph database is highly beneficial for a recommender system because it can efficiently handle complex and interconnected data. 

In such databases, data is stored as nodes and edges, representing entities and their relationships. This structure is inherently suitable for recommender systems, which rely heavily on relationship analysis and pattern recognition. 

Graph databases excel in identifying connections and patterns among large datasets, enabling more accurate and personalized recommendations based on user preferences, behavior, and network relationships. This leads to a more intuitive and relevant user experience in recommendation scenarios.

For this project, I am using - Neo4j

## Getting Started

### Prerequisites
- Neo4j
- Python 3
- Neo4j Python driver

### Installation
1. Clone the repository:
    ```git clone [repository URL]```
2. Install required Python packages:
    ```pip install -r requirements.txt```


### Quickstart
Run the `import_data_and_enter_into_database.py` script to set up the database:
    ```python import_data_and_enter_into_database.py```

For recommendations, execute:
    ```python recommendation_system.py```


## Usage
Refer to [USAGE.md](src/docs/USAGE.md) for detailed instructions on using the system.

## Development
See `DEVELOPMENT.md` for information on system architecture, contributing guidelines, and development notes.

## License
This project is licensed under the [MIT License](src/docs/LICENSE).
