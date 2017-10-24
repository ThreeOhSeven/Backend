import unittest
import requests
import json
import app
from app.models import User
from app import db


class likesBpTests(unittest.TestCase):
    def setUp(self):
        client = app.create_app("development")
        client.testing = True
        self.app = client.test_client()

    def test_createUser(self):
        response = self.app.post('/account/create',
                                 data=json.dumps(dict(username=username,
                                                      email=email,
                                                      birthday=birthday)),
                                 content_type='application/json')
        response = json.loads(response.data.decode())
        assert response['result'], response['error']
        assert db.session.query(User).filter_by(username=username).first() is not None, "User not created"