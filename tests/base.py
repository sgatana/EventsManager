import unittest
from app import create_app, db

class BaseTest(unittest.TestCase):

    config_name = 'testing'
    app = create_app(config_name)

    def setUp(self):
        with self.app.app_context():
            db.create_all()
            db.session.commit()
            self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.session.remove()

