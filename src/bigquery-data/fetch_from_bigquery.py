import json
from google.cloud import bigquery


def get_all_orders_from_bigquery():
    """
    This function gets all orders from bigquery dataset
    :return: DataFrame containing all the order details
    """
    # Instantiate a BigQuery client
    client = bigquery.Client()

    # Define the SQL query
    query = 'SELECT order_id, user_id FROM `bigquery-public-data.thelook_ecommerce.orders`'

    # Run the query and convert the results to za DataFrame
    orders_df = client.query(query).to_dataframe()

    return orders_df


def get_user_details_from_bigquery(user_id: int):
    """
    This function gets the user details from the bigquery dataset using the user ID
    :param user_id:  id of user whose details to fetch
    :return: dict containing user details
    """
    # Instantiate a BigQuery client
    client = bigquery.Client()

    # Define the SQL query
    query = f'SELECT first_name, last_name FROM `bigquery-public-data.thelook_ecommerce.users` WHERE id = {user_id}'

    # Run the query and convert the results to DataFrame
    user_details = client.query(query).to_dataframe()

    # Add user id in user details
    user_details['id'] = user_id

    # Convert user details to json format and return
    return json.loads(user_details.to_json(orient='records'))[0]


def get_product_ids_from_bigquery(order_id: int):
    """
    This function uses the order ID and fetches a list of the product IDs of all the products in the order
    :param order_id:  id used to fetch product ids
    :return: list containing all the product ids
    """
    # Instantiate a BigQuery client
    client = bigquery.Client()

    # Define the SQL query
    query = f'SELECT product_id FROM `bigquery-public-data.thelook_ecommerce.order_items` WHERE order_id = {order_id}'

    # Run the query and convert the results to DataFrame
    product_ids = client.query(query).to_dataframe()

    # Extracting the list of product_ids and return
    return product_ids['product_id'].tolist()


def get_product_details_from_bigquery(product_id: int):
    """
    This function gets the product details from the bigquery dataset using the product ID
    :param product_id: id of product whose details to fetch
    :return: dict containing product details
    """
    # Instantiate a BigQuery client
    client = bigquery.Client()

    # Define the SQL query
    query = f'SELECT name, category FROM `bigquery-public-data.thelook_ecommerce.products` WHERE id = {product_id}'

    # Run the query and convert the results to DataFrame
    product_details = client.query(query).to_dataframe()

    # Add product id in user details
    product_details['id'] = product_id

    # Convert product details to json format and return
    return json.loads(product_details.to_json(orient='records'))[0]
