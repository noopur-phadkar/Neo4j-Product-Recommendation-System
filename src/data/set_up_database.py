import requests
from neo4j import GraphDatabase

product_url = "https://fakestoreapi.com/products"
user_url = "https://fakestoreapi.com/users"
cart_url = "https://fakestoreapi.com/carts"
category_url = "https://fakestoreapi.com/products/categories"


def get_neo4j_driver():
    """
    # Set up Neo4j credentials
    :return: Neo4j Connection Driver
    """
    neo_uri = "bolt://localhost:7687"
    neo_user = "neo4j"
    neo_password = "password"
    return GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))       # establish and return Neo4j connection


def create_product_node(tx, product):
    """
    This function runs the cypher query for creating Product node.
    :param tx: Transaction to be run
    :param product: Product data
    :return: Result Object
    """
    tx.run(
        """
        CREATE (:Product {id: $id, title: $title, price: $price, description: $description, category_name: $category_name, image: $image, rating_rate: $rating_rate, rating_count: $rating_count})
        """,
        id=product['id'],
        title=product['title'],
        price=product['price'],
        description=product['description'],
        category_name=product['category'],
        image=product['image'],
        rating_rate=product['rating']['rate'],
        rating_count=product['rating']['count']
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
            session.write_transaction(create_product_node, product)

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
        CREATE (:User {id: $id, email: $email, username: $username, password: $password, firstname: $firstname, lastname: $lastname, phone: $phone, street: $street, number: $number, city: $city, zipcode: $zipcode, latitude: $latitude, longitude: $longitude})
        """,
        id=user['id'],
        email=user['email'],
        username=user['username'],
        password=user['password'],
        firstname=user['name']['firstname'],
        lastname=user['name']['lastname'],
        phone=user['phone'],
        street=user['address']['street'],
        number=user['address']['number'],
        city=user['address']['city'],
        zipcode=user['address']['zipcode'],
        latitude=user['address']['geolocation']['lat'],
        longitude=user['address']['geolocation']['long']
    )


def create_user_nodes(neo_driver):
    """
Function to create user nodes in Neo4j    :param neo_driver: Neo4j Connection Driver
    :return: None
    """
    users = requests.get(user_url).json()               # Fetch user data from API

    with neo_driver.session() as session:
        for user in users:
            session.write_transaction(create_user_node, user)


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
                quantity = product['quantity']
                # Establish 'Purchased' relationship between user and product
                session.run(
                    """
                    MATCH (u:User {id: $user_id})
                    MATCH (p:Product {id: $product_id})
                    CREATE (u)-[:PURCHASED {quantity: $quantity}]->(p)
                    """,
                    user_id=user_id,
                    product_id=product_id,
                    quantity=quantity
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
    neo_driver = get_neo4j_driver()                         # Get the Neo4j Connection Driver
    process_categories(neo_driver)                          # Create category nodes in Neo4j
    create_product_nodes(neo_driver)                        # Create product nodes in Neo4j
    create_user_nodes(neo_driver)                           # Create user nodes in Neo4j
    process_cart_data(neo_driver)                           # Create user nodes in Neo4j


if __name__ == '__main__':
    import_data_and_enter_into_database()
