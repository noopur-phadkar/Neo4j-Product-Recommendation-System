from google.cloud import bigquery
import os


def get_user_details(user_id):
    # Instantiate a BigQuery client
    client = bigquery.Client()
    # Define the SQL query
    query = f'SELECT first_name, last_name FROM `bigquery-public-data.thelook_ecommerce.users` WHERE id = {user_id}'
    # Run the query and convert the results to za DataFrame
    user_details = client.query(query).to_dataframe()
    return user_details


def main():
    # Replace 'your-gcp-project-id' with your actual Google Cloud project ID
    os.environ["GCLOUD_PROJECT"] = "your-project-name"

    # Instantiate a BigQuery client
    client = bigquery.Client()

    # Define the SQL query
    query = 'SELECT order_id, user_id FROM `bigquery-public-data.thelook_ecommerce.orders`'

    # Run the query and convert the results to za DataFrame
    orders_df = client.query(query).to_dataframe()
    for _, row in orders_df.iterrows():
        order_id = row['order_id']
        user_id = row['user_id']
        print(get_user_details(user_id))
        break


if __name__ == '__main__':
    main()
