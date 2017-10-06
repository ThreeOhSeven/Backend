from app import db
from sqlalchemy.orm import validates
from datetime import datetime

class User(db.Model):
    """
         Create the Users table
    """

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    birthday = db.Column(db.DateTime, nullable=True)

    # friend_to = db.relationship('Friend', backref='to', primaryjoin='User.id==Friend.user_to')
    # friend_from = db.relationship('Friend', backref='from', primaryjoin='User.id==Friend.user_from')

    def __init__(self, username, email, birthday):
        self.username = username
        self.email = email
        self.birthday = birthday

    @validates('username')
    def validate_username(self, key, username):
        assert db.session.query(User).filter_by(username=username).first() is not None, "Username taken"
        return username

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, 'Invalid email'
        return email

    @validates('birthday')
    def validate_birthday(self, key, birthday):
        # assert datetime.strptime(birthday, '%Y/%m/%d'), "Invalid date"
        return birthday


    def __repr__(self):
        return '<User id: {}, Username: {}, Email: {}, Birthday: {}>'.format(self.id, self.username, self.email, self.birthday)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Bet(db.Model):
    """
        Create a Bet table
    """

    __tablename__ = 'Bets'

    id = db.Column(db.Integer, primary_key=True)
    max_users = db.Column(db.String(60))
    title = db.Column(db.String(60), nullable=False)
    text = db.Column(db.String(255))
    amount = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, max_users, title, text, amount):
        self.max_users = max_users
        self.title = title
        self.text = text
        self.amount = amount

    def __repr__(self):
        return '<Bet id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bet.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
