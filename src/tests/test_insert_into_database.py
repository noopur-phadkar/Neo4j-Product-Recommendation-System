import unittest
from unittest.mock import MagicMock, ANY
from src.database.insert_into_database import InsertIntoDB


class TestInsertIntoDB(unittest.TestCase):

    def setUp(self):
        # Setup your test environment
        self.db = InsertIntoDB()
        self.db.driver = MagicMock()  # Mock the database connection

    def test_check_user_in_database(self):
        # Mock the result of the database query
        self.db.driver.session().run().single.return_value = None
        self.assertFalse(self.db.check_user_in_database('123'))
        self.db.driver.session().run().single.return_value = True
        self.assertTrue(self.db.check_user_in_database('123'))

    def test_check_product_in_database(self):
        self.db.driver.session().run().single.return_value = None
        self.assertFalse(self.db.check_product_in_database('101'))
        self.db.driver.session().run().single.return_value = True
        self.assertTrue(self.db.check_product_in_database('101'))

    def test_check_category_in_database(self):
        self.db.driver.session().run().single.return_value = None
        self.assertFalse(self.db.check_category_in_database('Electronics'))
        self.db.driver.session().run().single.return_value = True
        self.assertTrue(self.db.check_category_in_database('Electronics'))

    def test_create_user_node(self):
        user_details = {'id': '123', 'name': {'firstname': 'John', 'lastname': 'Doe'}}
        self.db.create_user_node(user_details)
        self.db.driver.session().run.assert_called_with(ANY)

    def test_create_product_node(self):
        product_details = {'id': '101', 'title': 'Smartphone'}
        self.db.create_product_node(product_details)
        self.db.driver.session().run.assert_called_with(ANY)

    def test_create_category_node(self):
        category_details = {'name': 'Electronics'}
        self.db.create_category_node(category_details)
        self.db.driver.session().run.assert_called_with(ANY)

    def test_create_relationship_user_to_product(self):
        user_details = {'id': '123'}
        product_details = {'id': '101'}
        self.db.create_relationship_user_to_product(user_details, product_details)
        self.db.driver.session().run.assert_called_with(ANY)

    def test_create_relationship_products_to_categories(self):
        product_details = {'id': '101'}
        category_details = {'name': 'Electronics'}
        self.db.create_relationship_products_to_categories(category_details, product_details)
        self.db.driver.session().run.assert_called_with(ANY)


if __name__ == '__main__':
    unittest.main()
