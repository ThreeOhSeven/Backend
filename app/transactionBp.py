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

import calendar
import time

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

@transactionRoutes.route("/payment/payout", methods = ["POST"])
def processPayout():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        authClass = authBackend()
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        stripeToken = payload['stripeToken']
        print("stripe token: ", stripeToken)
        payoutAmt = int(payload['payoutAmount']) * 100
        try:
            try:
                bcOb = BlockchainTransact()
                fundCheck = bcOb.verify_payout(email, payoutAmt)
                if not fundCheck:
                    return jsonify({'result' : False, 'error' : "Insufficient Funds"})
            except Exception as e:
                print("error with blockchain", e)
                return jsonify({'result' : False, 'error' : "Some error with blockchain"}), 400
            #process payout here
            try:
                allAccounts = stripe.Account.list(limit=3)
                target_account = None
                for account in allAccounts:
                    if account['email'] == email:
                        target_account = account
                        break
                if target_account is None:
                    print("no stripe account")
                    return jsonify({'result' : False, 'error' : "This will not work for tomorrow"})

                target_account_id = target_account['id']
                transfer = stripe.Transfer.create(amount = payoutAmt, currency = "usd", destination=target_account_id)
                payout = stripe.Payout.create(amount = payoutAmt, currency = "usd", stripe_account=target_account_id)
                return jsonify({'result' : True})
            except Exception as e:
                print("error with creating stripe recipient: ", e)
                return jsonify({'result' : False, 'error' : "Problem with creating Stripe recipient"})
            return jsonify({'result' : True, 'message' : "Payout Successful"})
        except Exception as e:
            print("error with stripe", e)
            return jsonify({'result' : False, 'error' : "error with payout"}), 400
    return jsonify({'result' : False, 'error' : "Invalid request"}), 400

@transactionRoutes.route("/payment/connectAccount", methods = ["POST"])
def createNewStripe():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        print(payload)
        token = payload['authToken']
        authClass = authBackend()
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        stripeToken = payload['stripeToken']
        print("stripe token: ", stripeToken)
        allAccounts = stripe.Account.list(limit=3)
        target_account = None
        for account in allAccounts:
            if account['email'] == email:
                target_account = account
                break

        if target_account is not None:
            return jsonify({'result' : False, 'error' : "Account with this email exists"})

        try:
            newAccount = stripe.Account.create(type="custom",country="US",email=email,external_account=stripeToken, tos_acceptance={'date': 1512106485,'ip': "128.210.106.73"})
            accountToSD = calendar.timegm(time.gmtime())
            accountToSI = request.remote_addr
            accountToS = {'date' : accountToSD, 'ip' : accountToSI}
            accountAddr = payload['address']
            accountFname = payload['firstName']
            accountLname = payload['lastName']
            accountzip = payload['postalCode']
            accountssn = payload['ssnLast4']
            accountState = payload['state']
            accountDobM = payload['dateOfBirth']['month']
            accountDobD = payload['dateOfBirth']['day']
            accountDobY = payload['dateOfBirth']['year']
            accountCi = payload['city']

            newAccount.legal_entity.first_name = accountFname
            newAccount.legal_entity.last_name = accountLname

            # newAccount.legal_entity.tos_acceptance.date = accountToSD
            # newAccount.legal_entity.tos_acceptance.ip = accountToSI

            newAccount.legal_entity.address.city = accountCi
            newAccount.legal_entity.address.line1 = accountAddr
            newAccount.legal_entity.address.postal_code = accountzip
            newAccount.legal_entity.address.state = accountState
            newAccount.legal_entity.ssn_last_4 = accountssn
            newAccount.legal_entity.dob.day = accountDobD
            newAccount.legal_entity.dob.month = accountDobM
            newAccount.legal_entity.dob.year = accountDobY

            newAccount.save()
            return jsonify({'result' : True})
        except Exception as e:
            print(e)
            return jsonify({'result' : False})

    return jsonify({'result' : False, 'error' : "Invalid request"}), 400
