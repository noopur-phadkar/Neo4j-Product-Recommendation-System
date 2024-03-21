import unittest
from src.database.database_setup import DatabaseSetup


class TestDatabaseConstraints(unittest.TestCase):

    def setUp(self):
        # Initialize the DatabaseSetup with your credentials
        self.db_setup = DatabaseSetup("bolt://localhost:7687", "neo4j", "password")
        # Clear the database for testing
        self.db_setup.clear_database()  # Implement this method to reset the database

    def test_unique_product_id_constraint(self):
        # Create a product node
        create_product_query = """
                CREATE (:Product {id: $id, title: $title, price: $price, description: $description, 
                                  category_name: $category_name, image: $image, 
                                  rating_rate: $rating_rate, rating_count: $rating_count})
                """

        # Insert a product
        product_data = {
            "id": 1,
            "title": "Test Product",
            "price": 10.99,
            "description": "Test Description",
            "category_name": "TestCategory",
            "image": "http://example.com/image.png",
            "rating_rate": 4.5,
            "rating_count": 100
        }
        # Insert the product
        with self.db_setup.driver.session() as session:
            session.run(create_product_query, **product_data)

        # Try to insert the same product again and expect an exception
        with self.assertRaises(Exception):
            with self.db_setup.driver.session() as session:
                session.run(create_product_query, **product_data)

    def tearDown(self):
        # Clean up and close the database connection after each test
        self.db_setup.close()


if __name__ == '__main__':
    unittest.main()
