from flask_testing import TestCase

from app import create_app, db, models


class MyTest(TestCase):

    def create_app(self):

        # pass in test configuration
        return create_app("testing")

    def setUp(self):

        db.create_all()

    def test_create_user(self):
        like = models.Likes()
        db.session.add(user)
        db.session.commit()

        # this works
        assert user in db.session

        response = self.client.get("/")

        # this raises an AssertionError
        assert user in db.session

    def tearDown(self):

        db.session.remove()
        db.drop_all()