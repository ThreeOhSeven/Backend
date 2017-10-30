from flask import request, jsonify, Blueprint

import json
from .models import User, Bet, BetUsers
from sqlalchemy import or_, and_
from .authRoutines import *

betUsersRoutes = Blueprint('betUsersBp', __name__)

authClass = authBackend()

@betUsersRoutes.route('/bets/join', methods=['POST'])
def join_bet():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    payload = json.loads(request.data.decode())
    token = payload['authToken']
    betID = payload['betID']
    side = payload['side']

    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(User).filter_by(email=email).first()
    bet = db.session.query(Bet).filter_by(id=betID).first()

    if user is None:
        return jsonify({'result': False, 'error': 'User not found'}), 400

    if bet is None:
        return jsonify({'result': False, 'error': 'Bet not found'}), 400

    # Check that the user has enough currency to join the bet
    userBalance = db.session.query(Transactions).filter_by(user_id=user.id).first()
    if userBalance.current_balance < bet.amount:
        return jsonify({'result': False, 'error': 'User\'s balance is too low.'}), 400

    # Add the user to the bet i.e. add an entry to BetUsers
    betUser = BetUsers(bet_id=betID, user_id=user.id, active=1, side=side)
    userBalance.current_balance -= bet.amount
    # Update the users current balance accordingly
    userBalance.save()
    betUser.save()

    return jsonify({'result': True, 'error': ''}), 200

@betUsersRoutes.route('/bets/send', methods=['POST'])
def send_bet():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    betID = payload['betID']
    id = payload['id']

    if authClass.decode_jwt(token) is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(User).filter_by(id=id).first()
    bet = db.session.query(Bet).filter_by(id=betID).first()

    if user is None:
        return jsonify({'result': False, 'error': 'User not found'}), 400

    if bet is None:
        return jsonify({'result': False, 'error': 'Bet not found'}), 400

    betUsersCount = db.session.query(BetUsers).filter_by(bet_id=bet.id).count()
    if betUsersCount is bet.max_users:
        return jsonify({'result': False, 'error': 'The bet is full'}), 400

    # Add the passive user to the bet
    betUser = BetUsers(bet_id=bet.id, user_id=user.id, active=0)
    betUser.save()

    return jsonify({'result': True, 'error': ''}), 200

@betUsersRoutes.route('/bets/accept', methods=['POST'])
def accept_bet():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    payload = json.loads(request.data.decode())
    token = payload['authToken']
    betID = payload['betID']
    side = payload['side']

    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(User).filter_by(email=email).first()
    bet = db.session.query(Bet).filter_by(id=betID).first()

    if user is None:
        return jsonify({'result': False, 'error': 'User not found'}), 400

    if bet is None:
        return jsonify({'result': False, 'error': 'Bet not found'}), 400

    # Check that the user has enough currency to join the bet
    userBalance = db.session.query(Transactions).filter_by(user_id=user.id).first()
    if userBalance.current_balance < bet.amount:
        return jsonify({'result': False, 'error': 'User\'s balance is too low.'}), 400

    # Update the users side, and convert them from passive to active.
    betUser = db.session.query(BetUsers).filter_by(and_(user_id=user.id, bet_id=betID)).first()
    betUser.side = side
    betUser.active = 1
    # Update the users balance accordingly
    userBalance.current_balance -= bet.amount
    userBalance.save()
    betUser.save()

    return jsonify({'result': True, 'error': ''}), 200

@betUsersRoutes.route('/bets/reject', methods=['POST'])
def reject_bet():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    payload = json.loads(request.data.decode())
    token = payload['authToken']
    betID = payload['betID']

    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(User).filter_by(email=email).first()
    bet = db.session.query(Bet).filter_by(id=betID).first()

    if user is None:
        return jsonify({'result': False, 'error': 'User not found'}), 400

    if bet is None:
        return jsonify({'result': False, 'error': 'Bet not found'}), 400

    # Remove the user from the bet entirely
    betUser = db.session.query(BetUsers).filter_by(and_(user_id=user.id, bet_id=betID)).first()
    db.session.delete(betUser)
    db.session.commit()

    return jsonify({'result': True, 'error': ''}), 200