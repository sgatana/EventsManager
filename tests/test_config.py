import unittest
import os
from config import app_config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.testing = app_config['testing']
        self.development = app_config['development']
        self.production = app_config['production']

    def test_testing_config(self):
        self.assertTrue(self.testing.DEBUG is True)
        self.assertTrue(self.testing.TESTING is True)
        self.assertTrue(self.testing.SQLALCHEMY_DATABASE_URI == os.environ.get('TESTDB_URL'))

    def test_development_config(self):
        self.assertTrue(self.development.DEBUG)
        self.assertFalse(self.development.SQLALCHEMY_DATABASE_URI == 'postgresql://localhost/db')
        self.assertFalse(self.development.SECRET_KEY is 'this is precious')

    def test_production_config(self):
        self.assertFalse(self.production.DEBUG)