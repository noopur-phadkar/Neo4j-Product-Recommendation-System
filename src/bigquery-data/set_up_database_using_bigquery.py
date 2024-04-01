import os
from fetch_from_bigquery import *
from src.database.insert_into_database import InsertIntoDB


class DBSetupUsingBigquery:

    def __init__(self):
        self.insert_into_db = InsertIntoDB()

    def import_data_and_enter_into_database(self):
        # Replace 'your-gcp-project-id' with your actual Google Cloud project ID
        os.environ["GCLOUD_PROJECT"] = "recommendation-system-418420"

        for _, row in get_all_orders_from_bigquery().iterrows():
            order_id = row['order_id']
            user_id = row['user_id']
            user_details = get_user_details_from_bigquery(user_id)
            for product_id in get_product_ids_from_bigquery(order_id):
                product_details = get_product_details_from_bigquery(product_id)
                category_details = {'name': product_details['category']}
                self.insert_into_db.insert_data_and_create_relationships(user_details, product_details, category_details)
            # if not self.check_user_in_database(user_id):
            #     self.insert_user_in_database(get_user_details_from_bigquery(user_id))
            # for product_id in get_product_ids_from_bigquery(order_id):
            #     if not self.check_product_in_database(product_id):
            #         self.insert_product_in_database(get_product_details_from_bigquery(product_id))


if __name__ == '__main__':
    setup_db_using_bigquery = DBSetupUsingBigquery()
    setup_db_using_bigquery.import_data_and_enter_into_database()
