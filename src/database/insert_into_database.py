from src.database.database_setup import DatabaseSetup


class InsertIntoDB:

    def __init__(self):
        # Initialize database setup
        db_setup = DatabaseSetup()
        # Clear database
        db_setup.clear_database()
        # You can add database setup related calls here if needed
        # db_setup.create_constraints()     #TODO
        self.driver = db_setup.driver

    def check_user_in_database(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {id: $id}) RETURN u", id=user_id
            )
            return result.single() is not None

    def check_product_in_database(self, product_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Product {id: $id}) RETURN p", id=product_id
            )
            return result.single() is not None

    def check_category_in_database(self, category_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category {name: $name}) RETURN c", name=category_name
            )
            return result.single() is not None

    def create_user_node(self, user_details):
        with self.driver.session() as session:
            try:
                session.run(
                    """
                    CREATE (:User {id: $id, firstname: $firstname, lastname: $lastname})
                    """,
                    id=user_details['id'],
                    firstname=user_details['name']['firstname'],
                    lastname=user_details['name']['lastname']
                )
            except Exception as e:
                print(f"Error occurred: {e}")  # Log the error or handle it as needed

    def create_product_node(self, product_details):
        with self.driver.session() as session:
            try:
                session.run(
                    """
                    CREATE (:Product {id: $id, title: $title})
                    """,
                    id=product_details['id'],
                    title=product_details['title'],
                )
            except Exception as e:
                print(f"Error occurred: {e}")  # Log the error or handle it as needed


    def create_category_node(self, category_details):
        with self.driver.session() as session:
            # Create Category node
            session.run(
                """
                CREATE (:Category {name: $name})
                """,
                name=category_details['name']
            )

    def create_relationship_products_to_categories(self, category_details, product_details):
        with self.driver.session() as session:
            # Create 'BelongsTo' relationship between product and category
            session.run(
                """
                MATCH (p:Product {id: $product_id})
                MATCH (c:Category {category_name: $category_name})
                CREATE (p)-[:BELONGS_TO]->(c)
                """,
                product_id=product_details['id'],
                category_name=category_details['name']
            )

    def create_relationship_user_to_product(self, user_details, product_details):
        """
        Function to process cart data and establish 'Purchased' relationship
        :param neo_driver: Neo4j Connection Driver
        :return: Nonw
        """
        with self.driver.session() as session:
            # Establish 'Purchased' relationship between user and product
            session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (p:Product {id: $product_id})
                CREATE (u)-[:PURCHASED]->(p)
                """,
                user_id=user_details['id'],
                product_id=product_details['id']
            )

    def insert_data_and_create_relationships(self, user_details, product_details, category_details):
        if not self.check_user_in_database(user_details['id']):
            self.create_user_node(user_details)
        if not self.check_product_in_database(product_details['id']):
            self.create_product_node(product_details)
        if not self.check_category_in_database(category_details['name']):
            self.create_category_node(category_details)
        self.create_relationship_user_to_product(user_details, product_details)
        self.create_relationship_products_to_categories(category_details, product_details)


if __name__ == '__main__':
    insert_into_db = InsertIntoDB()
    insert_into_db.insert_data_and_create_relationships({}, {},{})
