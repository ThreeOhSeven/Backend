import flask
from flask import request, jsonify, Blueprint
import json

from .models import User, Bet, BetUsers
from .transactionBp import transaction
from sqlalchemy import or_, and_
from .authRoutines import *

betUsersRoutes = Blueprint('betUsersBp', __name__)

authClass = authBackend()

@betUsersRoutes.route('/bets/join', methods=['POST'])
def join_bet():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Authenticate the token and extract values from the request
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

    # Check to see if the bet is full
    numOfUsers = BetUsers.query.filter_by(bet_id=bet.id).count()
    if numOfUsers >= int(bet.max_users):
        return jsonify({'result': False, 'error': 'The bet is full.'}), 400

    # Check that the user has enough currency to join the bet
    if user.current_balance < bet.amount:
        return jsonify({'result': False, 'error': 'User\'s balance is too low.'}), 400

    # Check if this request is an accept or a join
    betUser = db.session.query(BetUsers).filter(and_(BetUsers.user_id == user.id,
                                                        BetUsers.bet_id == bet.id)).first()
    if betUser is None:
        betUser = BetUsers(bet_id=betID, user_id=user.id, active=1, side=side)
    else:
        betUser.side = side
        betUser.active = 1
    betUser.save()

    # Update the user and bet balance accordingly
    if transaction(user.id, bet.id, bet.amount) is False:
        return jsonify({'result': True, 'error': 'Transaction error'}), 400

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

    # Check to see if the bet is full
    numOfUsers = BetUsers.query.filter_by(bet_id=bet.id).count()
    if numOfUsers >= int(bet.max_users):
        return jsonify({'result': False, 'error': 'The bet is full.'}), 400

    # Add the passive user to the bet
    betUser = BetUsers(bet_id=bet.id, user_id=user.id, active=0, side=0)
    betUser.save()

    return jsonify({'result': True, 'error': ''}), 200

@betUsersRoutes.route('/bets/accept', methods=['POST'])
def accept_bet():
    # Redirect to join_bet, using code 307 to preserve the HTTP POST
    return flask.redirect(flask.url_for('betUsersBp.join_bet'), code=307)

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
    betUser = db.session.query(BetUsers).filter(and_(BetUsers.user_id == user.id,
                                                        BetUsers.bet_id == bet.id)).first()
    if betUser is None:
        return jsonify({'result': False, 'error': 'User not invited to this bet.'}), 400

    db.session.delete(betUser)
    db.session.commit()

    return jsonify({'result': True, 'error': ''}), 200

@betUsersRoutes.route('/bets/update/side', methods=['POST'])
def update_side_bet():
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

    betUser = db.session.query(BetUsers).filter(and_(BetUsers.user_id == user.id,
                                                     BetUsers.bet_id == bet.id)).first()

    if betUser is None:
        return jsonify({'result': False, 'error': 'User not in the bet'}), 400

    betUser.side = side
    betUser.save()

    return jsonify({'result': True, 'error': ''}), 200