import unittest
import requests
import json
import app
from app.models import User
from app import db

username = "betchaTestUser23"
email = "testuser23@betcha.com"
birthday = "1990/01/01"

class UserBp_Tests(unittest.TestCase):
    def setUp(self):
        client = app.create_app("development")
        app.config.from_pyfile('config.py')
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

    def test_getInfo(self):
        user = client.db.session.query(User).filter_by(username=username).first()
        response = self.app.post('/account/info',
                                 data=json.dumps(dict(id=user.id)),
                                 content_type='application/json')
        response = json.loads(response.data.decode())
        assert response['result'], response['error']
        assert response['username'] == user.username and \
               response['email'] == user.email and \
               response['birthday'] == datetime.strptime(user.birthday, "%Y/%m/%d"), "Incorrect Info"

    def test_editInfo(self):
        newEmail = 'newEmail@betcha.com'
        accountInformation = ({'username': username,
                               'email': newEmail,
                               'birthday': birthday})
        response = self.app.post('/account/edit',
                                 data=json.dumps(dict(accountInformation=accountInformation)),
                                 content_type='application/json')
        response = json.loads(response.data.decode())
        assert response['result'], response['error']
        assert user.email == newEmail, "User email info not edited"

    def test_deleteUser(self):
        user = db.session.query(User).filter_by(username=username).first()
        response = self.app.post('/account/delete',
                                 data=json.dumps(dict(id=user.id)),
                                 content_type='application/json')
        response = json.loads(response.data.decode())
        assert response['result'], response['error']
        user = db.session.query(User).filter_by(username=username).first()
        assert user is None, "User not deleted"

if __name__ == '__main__':
    unittest.main()
