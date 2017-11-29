import unittest
import requests
import json
import os, sys
import datetime

import app
from app.models import Likes, User, Bet, Comment
from app import db


class TestLikes(unittest.TestCase):
    authToken = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoicGV0ZXJuam9uZXM5NUBnbWFpbC5jb20iLCJleHAiOjE1MDg5MTMz"
    "NDh9.sYtvAxjemJMx945gEjRminXuWOU2ayJS1WfMuyKoNqU")

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        self.temp_bet = Bet(21, 5, "Test bet", "This is for this test", 5, False, "Yes", "No", datetime.datetime.now())

    def test_like(self):

        like = 1

        response = self.client().post('/like/update',
                                 data=json.dumps(dict(authToken=self.authToken,
                                                      like=like,
                                                      betId=self.temp_bet.id)),
                                 content_type='application/json')
        response = json.loads(response.data.decode())
        assert response['result'], response['error']
        with self.app.app_context():
            assert Likes.query.filter_by(bet_id=self.temp_bet.id).first() is not None, "Like not created"

    def test_bet_create(self):
        authToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoicGV0ZXJuam9uZXM5NUBnbWFpbC5jb20iLCJleHAiOjE1MDg5MTMzNDh9.sYtvAxjemJMx945gEjRminXuWOU2ayJS1WfMuyKoNqU"

        response = self.client().post("/auth/login", data=json.dumps(dict(authToken=authToken)))

        self.assertEquals(json.loads(response.data.decode()), dict(result=True))

if __name__ == '__main__':
    unittest.main()