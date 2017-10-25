import unittest
import requests
import json
import app
from app.models import Likes
from app import db


class likesBpTests(unittest.TestCase):
    authToken = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoicGV0ZXJuam9uZXM5NUBnbWFpbC5jb20iLCJleHAiOjE1MDg5MTMz"
    "NDh9.sYtvAxjemJMx945gEjRminXuWOU2ayJS1WfMuyKoNqU")
    betId = 0

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_createLike(self):
        betId = 1
        like = 1

        response = self.client().post('/like/update',
                                 data=json.dumps(dict(authToken=self.authToken,
                                                      like=like,
                                                      betId=betId)),
                                 content_type='application/json')
        response = json.loads(response.data.decode())
        assert response['result'], response['error']
        with self.app.app_context():
            assert Likes.query.filter_by(bet_id=betId).first() is not None, "Like not created"

if __name__ == '__main__':
    unittest.main()