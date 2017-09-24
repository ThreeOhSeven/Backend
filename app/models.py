from app import db


class Bet(db.Model):
    """
        Create a Bet table
    """

    __tablename__ = 'bets'

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