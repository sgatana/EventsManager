import json
from .base import BaseTest


class TestEvents(BaseTest):
    def test_authenticated_users_can_add_events(self):
        register_data = json.dumps({
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "admin"
        })
        self.client.post('api/auth/register', data=register_data, content_type='application/json')
        login_data = json.dumps({
            "email": "admin@gmail.com",
            "password": "admin"
        })
        res = self.client.post('api/auth/login', data=login_data, content_type='application/json')
        message = json.loads(res.data)

        event = json.dumps({
            "name": "Learning",
            "description": "Educating developers on how to build a world class product",
            "location": "Andela Nairobi",
            "event_date": "7/4/2017"
        })
        self.headers = {
            'Authorization':'Bearer '+message["token"]
        }
        response = self.client.post('api/events', data=event, headers=self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
