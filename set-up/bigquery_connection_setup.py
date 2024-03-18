"""
This snippet demonstrates how to set up a basic connection with a Google BigQuery dataset using the google-cloud-bigquery library

To install the google-cloud-bigquery library using pip
pip install google-cloud-bigquery

Author: Noopur Phadkar
"""

from google.cloud import bigquery

# Set up credentials
# Replace 'path/to/your/credentials.json' with the path to your JSON key file.
# If running on Google Cloud, you don't need to specify the credentials explicitly.
credentials_path = 'path/to/your/credentials.json'
client = bigquery.Client.from_service_account_json(credentials_path)

# Define your project ID and dataset ID
project_id = 'your-project-id'
dataset_id = 'your-dataset-id'

# Construct a reference to the dataset
dataset_ref = client.dataset(dataset_id, project=project_id)

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

print('Dataset ID: {}'.format(dataset.dataset_id))
print('Full ID: {}'.format(dataset.full_dataset_id))
print('Project: {}'.format(dataset.project))
print('Tables:')
for table in client.list_tables(dataset):
    print('\t{}'.format(table.table_id))