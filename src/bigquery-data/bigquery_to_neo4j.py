"""
This script demonstrates how to export data from Google BigQuery and import it into Neo4j using the google-cloud-bigquery and neo4j libraries.

To install the required libraries using pip:
pip install google-cloud-bigquery neo4j pandas

Author: Noopur Phadkar
"""

from google.cloud import bigquery
from neo4j import GraphDatabase
import pandas as pd
from bigquery_connection_setup import get_bigquery_client, get_dataset

# Set up BigQuery credentials
credentials_path = 'credentials.json'  # Replace with the path to your JSON key file
bq_client = get_bigquery_client(credentials_path)

# Set up Neo4j credentials
neo_uri = "neo4j://localhost:7687"
neo_user = "your_neo4j_username"
neo_password = "your_neo4j_password"
neo_driver = GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))

# Define your BigQuery project ID, dataset ID, and table ID
bq_project_id = 'your_bigquery_project_id'
bq_dataset_id = 'your_bigquery_dataset_id'
bq_table_id = 'your_bigquery_table_id'

# BigQuery query
query = f"""
SELECT *
FROM `{bq_project_id}.{bq_dataset_id}.{bq_table_id}`
"""

# Execute the query
query_job = bq_client.query(query)

# Fetch results
results = query_job.result()

# Convert results to pandas DataFrame
df = pd.DataFrame(results)


# Function to import data into Neo4j
def import_data(tx, data):
    for index, row in data.iterrows():
        # Assuming data format matches your node structure
        tx.run("CREATE (:Node {property: $property})", property=row['property'])


# Import data into Neo4j
with neo_driver.session() as session:
    session.write_transaction(import_data, df)
