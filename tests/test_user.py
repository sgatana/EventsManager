import json
import unittest
from app import create_app, db


class TestUser(unittest.TestCase):
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

    def test_user_registration_success(self):
        data = json.dumps({
            'username': 'admin',
            'email': 'admin@gmail.com',
            'password': 'admin1234'
        })

        response = self.client.post('api/auth/register', data=data, content_type='application/json')
        data = json.loads(response.data)
        self.assertTrue(response.status_code == 201)
        self.assertIn('registration successful', data['message'])

    def test_user_registration_duplicate_email(self):
        data = json.dumps({
            'username': 'admin',
            'email': 'admin@gmail.com',
            'password': 'admin1234'
        })
        self.client.post('api/auth/register', data=data, content_type='application/json')
        new_user = json.dumps({
            'username': "admin1",
            'email':  'admin@gmail.com',
            'password': 'admin123'
        })
        response = self.client.post('api/auth/register', data=new_user, content_type='application/json')
        message = json.loads(response.data)
        self.assertEqual(response.status_code, 409)
        self.assertIn('user already exists', message['error'])

    def test_registered_user_login(self):
        data = json.dumps({
            "username": 'admin',
            "email": "admin@gmail.com",
            "password": "admin"
        })
        self.client.post('api/auth/register', data=data, content_type='application/json')
        response = self.client.post('api/auth/login', data=data, content_type='application/json')
        message = json.loads(response.data)
        print(message)
        self.assertEqual(response.status_code, 200)
        self.assertIn('login successful', message['message'])

    def test_unregistered_user_login(self):
        data = json.dumps({
            "username": 'admin',
            "email": "admin@gmail.com",
            "password": "admin"
        })
        post_data = json.dumps({
            "username": 'admin1',
            "email": "admin1@gmail.com",
            "password": "admin"
        })
        self.client.post('api/auth/register', data=data, content_type='application/json')
        response = self.client.post('api/auth/login', data=post_data, content_type='application/json')
        message = json.loads(response.data)
        print(message)
        self.assertEqual(response.status_code, 401)
        self.assertIn('login unsuccessful', message['error'])

