import requests
from src.database.database_setup import DatabaseSetup

product_url = "https://fakestoreapi.com/products"
user_url = "https://fakestoreapi.com/users"
cart_url = "https://fakestoreapi.com/carts"
category_url = "https://fakestoreapi.com/products/categories"


def create_product_node(tx, product):
    """
    This function runs the cypher query for creating Product node.
    :param tx: Transaction to be run
    :param product: Product data
    :return: Result Object
    """
    tx.run(
        """
        CREATE (:Product {id: $id, title: $title})
        """,
        id=product['id'],
        title=product['title'],
    )


def create_product_nodes(neo_driver):
    """
    This function calls the Product API and enters Product node into database.
    It also calls the function that creates the relationships between Product and Category nodes.
    :param neo_driver: Neo4j Connection Driver
    :return: None
    """
    products = requests.get(product_url).json()         # Fetch product data from API

    with neo_driver.session() as session:               # Create product nodes in Neo4j
        for product in products:
            try:
                session.write_transaction(create_product_node, product)  # or create_user_node for users
            except Exception as e:
                print(f"Error occurred: {e}")  # Log the error or handle it as needed

    relate_products_to_categories(neo_driver)           # Establish 'BelongsTo' relationships between products and categories


def relate_products_to_categories(neo_driver):
    """
    This function calls the Products API and creates the relationships required in the database
    :param neo_driver: Neo4j Connection Driver
    :return: None
    """
    products = requests.get(product_url).json()         # Fetch product data from API

    with neo_driver.session() as session:
        for product in products:
            category = product['category']
            product_id = product['id']
            # Create 'BelongsTo' relationship between product and category
            session.run(
                """
                MATCH (p:Product {id: $product_id})
                MATCH (c:Category {category_name: $category_name})
                CREATE (p)-[:BELONGS_TO]->(c)
                """,
                product_id=product_id,
                category_name=category
            )


def create_user_node(tx, user):
    """
    This function runs the cypher query for creating User node.
    :param tx: Transaction to be run
    :param user: User data
    :return:Result object
    """
    tx.run(
        """
        CREATE (:User {id: $id, , firstname: $firstname, lastname: $lastname})
        """,
        id=user['id'],
        firstname=user['name']['firstname'],
        lastname=user['name']['lastname']
    )


def create_user_nodes(neo_driver):
    """
Function to create user nodes in Neo4j    :param neo_driver: Neo4j Connection Driver
    :return: None
    """
    users = requests.get(user_url).json()               # Fetch user data from API

    with neo_driver.session() as session:
        for user in users:
            try:
                session.write_transaction(create_user_node, user)  # or create_user_node for users
            except Exception as e:
                print(f"Error occurred: {e}")  # Log the error or handle it as needed


def process_cart_data(neo_driver):
    """
    Function to process cart data and establish 'Purchased' relationship
    :param neo_driver: Neo4j Connection Driver
    :return: Nonw
    """
    carts = requests.get(cart_url).json()               # Fetch cart data from API

    with neo_driver.session() as session:
        for cart in carts:
            user_id = cart['userId']
            for product in cart['products']:
                product_id = product['productId']
                # Establish 'Purchased' relationship between user and product
                session.run(
                    """
                    MATCH (u:User {id: $user_id})
                    MATCH (p:Product {id: $product_id})
                    CREATE (u)-[:PURCHASED]->(p)
                    """,
                    user_id=user_id,
                    product_id=product_id
                )


def process_categories(neo_driver):
    """
    Function to fetch and process categories
    :param neo_driver: Neo4j Connection Driver
    :return: None
    """
    categories = requests.get(category_url).json()          # Fetch category data from API

    with neo_driver.session() as session:
        # Create Category nodes
        for category in categories:
            session.run(
                """
                CREATE (:Category {name: $name, category_name: $category_name})
                """,
                name=category,
                category_name=category
            )


def import_data_and_enter_into_database():
    """
    This function imports all the data and puts it into the neo4j datatbase
    :return: None
    """
    # Initialize database setup
    db_setup = DatabaseSetup()
    # You can add database setup related calls here if needed
    db_setup.create_constraints()

    process_categories(db_setup.driver)                          # Create category nodes in Neo4j
    create_product_nodes(db_setup.driver)                        # Create product nodes in Neo4j
    create_user_nodes(db_setup.driver)                           # Create user nodes in Neo4j
    process_cart_data(db_setup.driver)                           # Create user nodes in Neo4j


if __name__ == '__main__':
    import_data_and_enter_into_database()
