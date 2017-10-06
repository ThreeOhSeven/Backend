from app import db

class User(db.Model):
    """
         Create the Users table
    """

    __tabelname_ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)

    bets_in = db.relationship('BetUsers', backref='user', lazy=True)

    def __init__(self, id, username, email, birthday):
        self.id = id
        self.username = username
        self.email = email
        self.birthday = birthday

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

    bet_users = db.relationship('BetUsers', backref='bet', lazy=True)

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


class BetUsers(db.Model):
    """
        Create a BetUsers table
    """

    __tablename__ = 'BetUsers'

    bet_id = db.Column(db.Integer, db.ForeignKey('bet.id'),
                       nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                       nullable=False)


    def __init__(self, bet_id, user_id):
        bet_id = bet_id
        user_id = user_id

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
