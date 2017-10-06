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

    bets_created = db.relationship('Bet', backref='user', lazy=True)

    bets_in = db.relationship('BetUsers', backref='user', lazy=True)

    friend_to = db.relationship('Friend', backref='to', primaryjoin='User.id==Friend.user_to')
    friend_from = db.relationship('Friend', backref='from', primaryjoin='User.id==Friend.user_from')

    def __init__(self, username, email, birthday):
        self.username = username
        self.email = email
        self.birthday = birthday

    @validates('username')
    def validate_username(self, key, username):
        #assert db.session.query(User).filter_by(username=username).first() is not None, "Username taken"
        return username

    @validates('email')
    def validate_email(self, key, email):
        #assert '@' in email, 'Invalid email'
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
        return "user_to: {}, user_from {}, stats: {}".format(self.user_to, self.user_from, self.status)

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
    max_users = db.Column(db.String(60))
    title = db.Column(db.String(60), nullable=False)
    text = db.Column(db.String(255))
    amount = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    locked = db.Column(db.Boolean, default=False, nullable=False)

    bet_users = db.relationship('BetUsers', backref='bet', lazy=True)

    def __init__(self, creator_id, max_users, title, text, amount, locked):
        self.creator_id = creator_id
        self.max_users = max_users
        self.title = title
        self.text = text
        self.amount = amount
        self.locked = locked

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


class BetUsers(db.Model):
    """
        Create a BetUsers table
    """

    __tablename__ = 'BetUsers'

    id = db.Column(db.Integer, primary_key=True)

    bet_id = db.Column(db.Integer, db.ForeignKey('Bets.id'),
                       nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'),
                       nullable=False)


    def __init__(self, bet_id, user_id):
        self.bet_id = bet_id
        self.user_id = user_id

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
