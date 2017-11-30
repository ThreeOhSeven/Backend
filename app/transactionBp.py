from flask import Blueprint, json, request, jsonify
import requests
from sqlalchemy import or_, and_
from app import db
from .models import User, Bet, Transactions
from app.config import Config
import stripe
from .blockchain import *

transactionRoutes = Blueprint('transaction', __name__)
stripe.api_key = Config.STRIPE_TEST_KEY
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

        # user_points = db.session.query(User).filter_by(id=uid).first()
        bcOb = BlockchainTransact()
        user_points = bcOb.getBalance(email)

        return jsonify({'result' : True, 'current_balance' : user_points})
    return jsonify({'result' : False})


# Transactions are always user to bet postive or negative
def transaction(userID, betID, amount):
    bet = db.session.query(Bet).filter_by(id=betID).first()

    user = db.session.query(User).filter_by(id=userID).first()
    bcOb = BlockchainTransact()
    current_balance = bcOb.getBalance_from_uid(userID)

    if current_balance - amount >= 0 and bet.pot + amount >= 0:
        # user.current_balance -= amount
        bet.pot += amount
        # user.save()
        bet.save()
    else:
        return False

    if amount < 0:
        #bet to user
        result, tx = bcOb.newPayment_with_uid(userID, abs(amount))
        print("tx: ", tx)
        print("toUser: ", userID)
        # Record the transaction in the table
        transactionEntry = Transactions(userID, betID, amount)
        transactionEntry.save()
        return result
    else:
        #user to bet
        result, tx = bcOb.withdraw_from_user(userID, amount)
        print("tx: ", tx)
        print("fromUser: ", userID)

        # Record the transaction in the table
        transactionEntry = Transactions(userID, betID, amount)
        transactionEntry.save()
        return result

    return False

@transactionRoutes.route("/payment/charge", methods = ["POST"])
def chargeStripe():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        authClass = authBackend()
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        stripeToken = payload['stripeToken']
        print("stripe token: ", stripeToken)
        chargeAmt = payload['chargeAmount']
        try:
            try:
                bcOb = BlockchainTransact()
            except Exception as e:
                print("error with blockchain")
                return jsonify({'result' : False, 'error' : "Some error with blockchain"})
            charge = stripe.Charge.create(amount=chargeAmt, currency="usd", description="user deposit betcha", source = stripeToken)
            print("charge successful")
            blockchainPaySuccess = bcOb.newPayment(email, int(chargeAmt) / 100)
            return jsonify({'result' : True})
        except Exception as e:
            print(e)
            return jsonify({'result' : False, 'error' : "error with card charge"}), 400
    return jsonify({'result' : False, 'error' : "Invalid request"}), 400
