from flask import Blueprint, json, request, jsonify
import requests
from sqlalchemy import or_, and_
from app import db
from .models import User, Bet, Transactions

transactionRoutes = Blueprint('transaction', __name__)
from .authBp import authBackend

@transactionRoutes.route("/testRoute", methods = ["GET"])
def testRoute():
    return "Hello Transactions"

@transactionRoutes.route("/getPoints", methods = ["POST"])
def fetchPoints():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        authClass = authBackend()
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        user = db.session.query(User).filter_by(email=email).first()

        if user is None:
            return jsonify({'result': False, 'error': 'User not found'}), 400

        uid = user.id

        user_points = db.session.query(User).filter_by(id=uid).first()

        return jsonify({'result' : True, 'current_balance' : user_points.current_balance})
    return jsonify({'result' : False})

# Transactions are always user to bet postive or negative
def transaction(userID, betID, amount):
    bet = db.session.query(Bet).filter_by(id=betID).first()

    user = db.session.query(User).filter_by(id=userID).first()

    if user.current_balance - amount >= 0 and bet.pot + amount >= 0:
        user.current_balance -= amount
        bet.pot += amount
        user.save()
        bet.save()
    else:
        return False

    # Record the transaction in the table
    Transactions(userID, betID, amount)
    return True