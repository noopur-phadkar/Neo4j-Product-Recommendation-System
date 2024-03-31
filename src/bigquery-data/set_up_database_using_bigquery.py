import os

from fetch_from_bigquery import *


def check_user_in_database(user_id):  # TODO
    return True


def insert_user_in_database(user_details):  # TODO
    pass


def check_product_in_database(product_id):
    return True


def insert_product_in_database(product_details):
    if not check_product_in_database(product_details['id']):
        # insert into database
        pass


def import_data_and_enter_into_database():
    for _, row in get_all_orders_from_bigquery().iterrows():
        order_id = row['order_id']
        user_id = row['user_id']
        if not check_user_in_database(user_id):
            insert_user_in_database(get_user_details_from_bigquery(user_id))
        for product_id in get_product_ids_from_bigquery(order_id):
            if not check_product_in_database(product_id):
                insert_product_in_database(get_product_details_from_bigquery(product_id))


if __name__ == '__main__':
    import_data_and_enter_into_database()
