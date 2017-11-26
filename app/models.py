from app import db
import string
import random
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

    bets_created = db.relationship('Bet', backref='user', lazy=True,
                                   cascade='all, delete-orphan')

    bets_in = db.relationship('BetUsers', backref='user', lazy=True,
                              cascade='all, delete-orphan')

    bets_liked = db.relationship('Likes', backref='user', lazy=True,
                                 cascade='all, delete-orphan')

    friend_to = db.relationship('Friend', backref='to', primaryjoin='User.id==Friend.user_to',
                                cascade="all, delete-orphan")

    friend_from = db.relationship('Friend', backref='from', primaryjoin='User.id==Friend.user_from',
                                  cascade="all, delete-orphan")

    current_balance = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.String(256), unique=True, nullable=True)
    wins = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)

    def __init__(self, username, email, birthday, current_balance=10):
        self.username = username
        self.email = email
        self.birthday = birthday
        self.current_balance = current_balance

    def __repr__(self):
        return 'id: {}, Username: {}, Email: {}, Birthday: {}'.format(self.id, self.username, self.email, self.birthday)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def toJSON(self):
        obj = {
            "id" : self.id,
            "username" : self.username,
            "email" : self.email,
            "birthday" : self.birthday
        }

        return obj


class Friend(db.Model):
    """
        Create the Friends table
    """

    __tablename__ = 'Friends'

    user_to = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    user_from = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    status = db.Column(db.Integer)

    def __init__(self, user_to, user_from, status):
        self.user_to = user_to
        self.user_from = user_from
        self.status = status

    def __repr__(self):
        return "user_to: {}, user_from {}, status: {}".format(self.user_to, self.user_from, self.status)

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
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    max_users = db.Column(db.Integer)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255))
    amount = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.Boolean)
    locked = db.Column(db.Boolean, default=False, nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)
    pot = db.Column(db.Integer, nullable=False, default=0)
    side_a = db.Column(db.String(60), nullable=False, default='Yes')
    side_b = db.Column(db.String(60), nullable=False, default='No')
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    color = db.Column(db.Integer, nullable=True)
    icon = db.Column(db.Integer, nullable=True)

    # One to Many
    bet_users = db.relationship('BetUsers', backref='bet', lazy=True)
    likes = db.relationship('Likes', backref='bet', lazy=True)
    transactions = db.relationship('Transactions', backref='bet', lazy=True)

    def __init__(self, creator_id, max_users, title, description, amount, locked, side_a, side_b, creation_time):
        self.creator_id = creator_id
        self.max_users = max_users
        self.title = title
        self.description = description
        self.amount = amount
        self.locked = locked
        self.side_a = side_a
        self.side_b = side_b
        self.creation_time = creation_time
        self.color = random.randint(0,9)
        self.icon = random.randint(0, 9)


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

    @property
    def toJSON(self):
        obj = {
            'id': self.id,
            'creatorId': self.creator_id,
            'maxUsers': self.max_users,
            'title': self.title,
            'description': self.description,
            'amount': self.amount,
            'winner': self.winner,
            'locked': self.locked,
            'complete': self.complete,
            'sideA': self.side_a,
            'sideB': self.side_b,
            'creationTime': self.creation_time,
            'color': self.color,
            'icon': self.icon
        }

        return obj


class BetUsers(db.Model):
    """
        Create a BetUsers table
    """

    __tablename__ = 'BetUsers'

    id = db.Column(db.Integer, primary_key=True)
    bet_id = db.Column(db.Integer, db.ForeignKey('Bets.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    side = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Integer, nullable=False, default=2)


    def __init__(self, bet_id, user_id, active, side):
        self.bet_id = bet_id
        self.user_id = user_id
        self.active = active
        self.side = side

    def __repr__(self):
        return '<BetUsers id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return BetUsers.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Likes(db.Model):
    """
        Create the Likes table
    """

    __tablename__ = 'Likes'

    id = db.Column(db.Integer, primary_key=True)

    bet_id = db.Column(db.Integer, db.ForeignKey('Bets.id'),
                       nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'),
                       nullable=False)



    def __init__(self, bet_id, user_id):
        self.bet_id = bet_id
        self.user_id = user_id

    def __repr__(self):
        return '<Like id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Likes.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Transactions(db.Model):

    __tablename__ = 'Transactions'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    bet_id = db.Column(db.Integer, db.ForeignKey('Bets.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, bet_id, amount):
        self.user_id = user_id
        self.bet_id = bet_id
        self.amount = amount

    def __repr__(self):
        return '<Transactions id: {}>'.format(self.id)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Transactions.query.all()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

class AddressBook(db.Model):

    __tablename__ = 'AddressBook'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    account_hex = db.Column(db.Text, nullable=False)
    bc_passphrase = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, account_hex, bc_passphrase):
        self.user_id = user_id
        self.account_hex = account_hex
        self.bc_passphrase = bc_passphrase

    def __repr__(self):
        return '<Account id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
