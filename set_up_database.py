import requests
from neo4j import GraphDatabase


def create_product_node(tx, product):
    tx.run(
        """
        CREATE (:Product {id: $id, title: $title, price: $price, description: $description, category: $category, image: $image, rating_rate: $rating_rate, rating_count: $rating_count})
        """,
        id=product['id'],
        title=product['title'],
        price=product['price'],
        description=product['description'],
        category=product['category'],
        image=product['image'],
        rating_rate=product['rating']['rate'],
        rating_count=product['rating']['count']
    )


def create_product_nodes(products):
    # Set up Neo4j credentials
    neo_uri = "bolt://localhost:7687"
    neo_user = "neo4j"
    neo_password = "password"

    # Establish Neo4j connection
    neo_driver = GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))

    # Create product nodes in Neo4j
    with neo_driver.session() as session:
        for product in products:
            session.write_transaction(create_product_node, product)


def create_user_node(tx, user):
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


# Function to create user nodes in Neo4j
def create_user_nodes(users):
    # Set up Neo4j credentials
    neo_uri = "bolt://localhost:7687"
    neo_user = "neo4j"
    neo_password = "password"
    neo_driver = GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))
    with neo_driver.session() as session:
        for user in users:
            session.write_transaction(create_user_node, user)


# Function to process cart data and establish 'Purchased' relationship
def process_cart_data(carts):
    # Set up Neo4j credentials
    neo_uri = "bolt://localhost:7687"
    neo_user = "neo4j"
    neo_password = "password"
    neo_driver = GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))

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


def main():
    # Fetch product data from API
    product_url = "https://fakestoreapi.com/products"
    products = requests.get(product_url).json()
    create_product_nodes(products)  # Create product nodes in Neo4j

    # Fetch user data from API
    user_url = "https://fakestoreapi.com/users"
    users = requests.get(user_url).json()
    create_user_nodes(users)  # Create user nodes in Neo4j

    # Fetch cart data from API
    cart_url = "https://fakestoreapi.com/carts"
    carts = requests.get(cart_url).json()
    process_cart_data(carts)  # Create user nodes in Neo4j


if __name__ == '__main__':
    main()
