import json
import os

from google.cloud import bigquery


def get_user_details(user_id):
    # Instantiate a BigQuery client
    client = bigquery.Client()
    # Define the SQL query
    query = f'SELECT first_name, last_name FROM `bigquery-public-data.thelook_ecommerce.users` WHERE id = {user_id}'
    # Run the query and convert the results to Dict
    user_details = client.query(query).to_dataframe()
    user_details['id'] = user_id
    user_details = json.loads(user_details.to_json(orient='records'))
    return user_details


def get_product_ids(order_id):
    # Instantiate a BigQuery client
    client = bigquery.Client()
    # Define the SQL query
    query = f'SELECT product_id FROM `bigquery-public-data.thelook_ecommerce.order_items` WHERE order_id = {order_id}'
    # Run the query and convert the results to DataFrame
    product_ids = client.query(query).to_dataframe()
    # Extracting the list of product_ids
    product_ids = product_ids['product_id'].tolist()
    return product_ids


def get_product_details(product_id):
    # Instantiate a BigQuery client
    client = bigquery.Client()
    # Define the SQL query
    query = f'SELECT name, category FROM `bigquery-public-data.thelook_ecommerce.products` WHERE id = {product_id}'
    # Run the query and convert the results to DataFrame
    product_details = client.query(query).to_dataframe().to_json()
    return product_details


def main():
    # Replace 'your-gcp-project-id' with your actual Google Cloud project ID
    os.environ["GCLOUD_PROJECT"] = "recommendation-system-418420"

    # Instantiate a BigQuery client
    client = bigquery.Client()

    # Define the SQL query
    query = 'SELECT order_id, user_id FROM `bigquery-public-data.thelook_ecommerce.orders`'

    # Run the query and convert the results to za DataFrame
    orders_df = client.query(query).to_dataframe()
    for _, row in orders_df.iterrows():
        order_id = row['order_id']
        user_id = row['user_id']
        user_details = get_user_details(user_id)
        print(user_details)
        product_ids = get_product_ids(order_id)
        for product_id in product_ids:
            product_details = get_product_details(product_id)
            print(product_details)
        break


if __name__ == '__main__':
    main()
