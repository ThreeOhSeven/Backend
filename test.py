import unittest
import requests
import json
import os, sys
import datetime

import app
from app.models import Likes, User, Bet, Comment
from app import db

authToken = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoicGV0ZXJuam9uZXM5NUBnbWFpbC5jb20iLCJleHAiOjE1MDg5MTMz"
    "NDh9.sYtvAxjemJMx945gEjRminXuWOU2ayJS1WfMuyKoNqU")


class TestLikes(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_like(self):
        with self.app.app_context():
            temp_bet = Bet(21, 5, "Test bet", "This is for this test", 5, False, "Yes", "No",
                                datetime.datetime.now())
            temp_bet.save()
            # this works
            assert temp_bet in db.session

            id = temp_bet.id

        like = 1

        with self.app.app_context():
            response = self.client().post('/like/update',
                                     data=json.dumps(dict(authToken=authToken,
                                                          like=like,
                                                          betId=id)),
                                     content_type='application/json')

        response = json.loads(response.data.decode())

        assert response['result'] is True

        with self.app.app_context():
            bet = Bet.query.filter_by(id=id).first()
            db.session.delete(bet)
            db.session.commit()


class TestBets(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_bet(self):

        data = json.dumps(dict(
            authToken=authToken,
            maxUsers=5,
            title="This is a create bet test",
            description="HELLO TEST",
            amount=5,
            locked='False',
            sideA="Yes",
            sideB="No"
        ))

        with self.app.app_context():
            response = self.client().post('/bets/create',
                                     data=data,
                                     content_type='application/json')

        response = json.loads(response.data.decode())

        assert response['result'] is True

        with self.app.app_context():
            bet = Bet.query.filter_by(id=id).first()
            assert bet is not None
            db.session.delete(bet)
            db.session.commit()


class TestComments(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

            temp_bet = Bet(21, 5, "Test bet", "This is for this test", 5, False, "Yes", "No",
                           datetime.datetime.now())
            temp_bet.save()

            self.id = temp_bet.id

    def test_create_comment(self):

        comment_text = "This comment is for the comment test"

        data = json.dumps(dict(
            authToken=authToken,
            betId=self.id,
            text=comment_text
        ))

        with self.app.app_context():
            response = self.client().post('/comment/add',
                                     data=data,
                                     content_type='application/json')

        response = json.loads(response.data.decode())

        assert response['result'] is True, "Endpoint failed"

        with self.app.app_context():
            assert Comment.query.filter_by(betId=self.id, text=comment_text).first() is not None, "Comment not created"

    def test_delete_comment(self):
        with self.app.app_context():
            temp_comment = Comment(21, self.id, "THIS IS FOR DELETING COMMENTS TEST")
            temp_comment.save()

            comment_id = temp_comment.id

        data = json.dumps(dict(
            authToken=authToken,
            commentId=comment_id
        ))

        with self.app.app_context():
            response = self.client().post('/comment/delete',
                                     data=data,
                                     content_type='application/json')

        response = json.loads(response.data.decode())

        assert response['result'] is True

        with self.app.app_context():
            assert Comment.query.filter_by(id=comment_id).first() is None

    def test_get_comment(self):
        with self.app.app_context():
            temp_comment = Comment(21, self.id, "THIS IS FOR GETTING COMMENTS TEST")
            temp_comment.save()

            comment_json = temp_comment.toJSON

        data = json.dumps(dict(
            authToken=authToken,
            betId=self.id
        ))

        with self.app.app_context():
            response = self.client().post('/comment/delete',
                                          data=data,
                                          content_type='application/json')

        response = json.loads(response.data.decode())

        assert response['result'] is True

        with self.app.app_context():
            assert response['comments'][0] is comment_json

    def tearDown(self):
        with self.app.app_context():
            bet = Bet.query.filter_by(id=self.id).first()
            assert bet is not None
            bet.delete()


if __name__ == '__main__':
    unittest.main(warnings='ignore')