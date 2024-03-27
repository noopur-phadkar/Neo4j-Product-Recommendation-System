from neo4j import GraphDatabase


class ProductRecommender:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_user_based_recommendations(self, target_user_id, top_n=5):
        query = """
        MATCH (target:User {id: $user_id})-[:PURCHASED]->(p:Product)
        MATCH (similar:User)-[:PURCHASED]->(p)
        WHERE NOT similar = target
        WITH similar, COUNT(*) AS shared
        ORDER BY shared DESC LIMIT 10

        MATCH (similar)-[:PURCHASED]->(recommended:Product)
        WHERE NOT (target)-[:PURCHASED]->(recommended)
        RETURN recommended.title AS Product, COUNT(*) AS Frequency
        ORDER BY Frequency DESC LIMIT $top_n
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=target_user_id, top_n=top_n)
            return [record["Product"] for record in result]

    def get_category_based_recommendations(self, target_user_id, top_n=5):
        query = """
        MATCH (u:User {id: $user_id})-[:PURCHASED]->(p:Product)-[:BELONGS_TO]->(c:Category)
        WITH u, p, c, c.category_name as category, COUNT(c) AS cnt ORDER BY COUNT(c) DESC LIMIT 1
        MATCH (:Category {category_name: category})<-[:BELONGS_TO]-(q:Product)
        WHERE NOT (u)-[:PURCHASED]->(q)
        RETURN category, q.title AS Recommendation
        ORDER BY category LIMIT $top_n
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=target_user_id, top_n=top_n)
            return [record["Recommendation"] for record in result]


if __name__ == "__main__":
    neo_uri = "bolt://localhost:7687"
    neo_user = "neo4j"
    neo_password = "password"

    recommender = ProductRecommender(neo_uri, neo_user, neo_password)
    user_id = "1"  # Replace with the actual target user ID

    print("User-Based Recommendations:", recommender.get_user_based_recommendations(user_id))
    print("Item-Based Recommendations:", recommender.get_item_based_recommendations(user_id))
    print("Category-Based Recommendations:", recommender.get_category_based_recommendations(user_id))

    recommender.close()
