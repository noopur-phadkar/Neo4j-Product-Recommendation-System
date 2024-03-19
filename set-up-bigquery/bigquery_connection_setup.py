"""
This snippet demonstrates how to set up a basic connection with a Google BigQuery dataset using the google-cloud-bigquery library

To install the google-cloud-bigquery library using pip
pip install google-cloud-bigquery

Author: Noopur Phadkar
"""

from google.cloud import bigquery

def get_bigquery_client(credentials_path):
    """Function to get a BigQuery client"""
    return bigquery.Client.from_service_account_json(credentials_path)

def get_dataset(client, project_id, dataset_id):
    """Function to get a dataset from BigQuery"""
    dataset_ref = client.dataset(dataset_id, project=project_id)
    return client.get_dataset(dataset_ref)

def list_tables(client, dataset):
    """Function to list tables in a dataset"""
    return [table.table_id for table in client.list_tables(dataset)]
