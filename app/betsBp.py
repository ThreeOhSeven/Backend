from flask import request, jsonify, abort, Blueprint

import math
import json
from app import models
from .authRoutines import *
from .transactionBp import transaction

from sqlalchemy import or_, and_
from pyfcm import FCMNotification

betRoutes = Blueprint('betsBp', __name__)

authClass = authBackend()

#######################################################################################
####                                     FEEDS                                     ####
#######################################################################################

######## Public Feed ########
@betRoutes.route('/publicfeed', methods=['POST'])
def public_feed():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:

            bets = models.Bet.get_all()
            results = []

            for bet in bets:

                # Get like count
                count = models.Likes.query.filter_by(bet_id=bet.id).count()

                # Get if the current user liked the bet
                like = models.Likes.query.filter_by(bet_id=bet.id, user_id=user.id).count()

                if like is 1:
                    liked = True
                else:
                    liked = False

                # Get users in bet
                bet_users = models.BetUsers.query.filter_by(bet_id=bet.id).all()
                users = []

                for bet_user in bet_users:
                    user = models.User.query.filter_by(id=bet_user.user_id).first()

                    users.append(user.toJSON)

                # Make JSONobject
                obj = bet.toJSON

                obj['numLikes'] = count
                obj['liked'] = liked
                obj['users'] = users

                results.append(obj)

            response = jsonify({'bets': results})
            response.status_code = 200
            return response


######## Private Feed ########
@betRoutes.route('/privatefeed', methods=['POST'])
def private_feed():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:

            # Users Bets
            my_bets = models.Bet.query.filter_by(creator_id=user.id).all()
            results = []

            for bet in my_bets:

                # Get like count
                count = models.Likes.query.filter_by(bet_id=bet.id).count()

                # Get if the current user liked the bet
                like = models.Likes.query.filter_by(bet_id=bet.id, user_id=user.id).count()

                if like is 1:
                    liked = True
                else:
                    liked = False

                # Get users in bet
                bet_users = models.BetUsers.query.filter_by(bet_id=bet.id).all()
                users = []

                for bet_user in bet_users:
                    user = models.User.query.filter_by(id=bet_user.user_id).first()

                    users.append(user.toJSON)

                # Make JSONobject
                obj = bet.toJSON

                obj['numLikes'] = count
                obj['liked'] = liked
                obj['users'] = users

                results.append(obj)

            # Friends Side 1
            friends_one = models.Friend.query.filter_by(user_to=user.id, status=1).all()

            for friend_one in friends_one:
                friend_one_bets = models.Bet.query.filter_by(creator_id=friend_one.user_from).all()

                for friend_one_bet in friend_one_bets:
                    # Get like count
                    count = models.Likes.query.filter_by(bet_id=friend_one_bet.id).count()

                    # Get if the current user liked the bet
                    like = models.Likes.query.filter_by(bet_id=friend_one_bet.id, user_id=user.id).count()

                    if like is 1:
                        liked = True
                    else:
                        liked = False

                    # Get users in bet
                    bet_users = models.BetUsers.query.filter_by(bet_id=friend_one_bet.id).all()
                    users = []

                    for bet_user in bet_users:
                        user = models.User.query.filter_by(id=bet_user.user_id).first()

                        users.append(user.toJSON)

                    # Make JSONobject
                    obj = friend_one_bet.toJSON

                    obj['numLikes'] = count
                    obj['liked'] = liked
                    obj['users'] = users

                    results.append(obj)

            # Friends Side 2
            friends_two = models.Friend.query.filter_by(user_from=user.id, status=1).all()

            for friend_two in friends_two:
                friend_two_bets = models.Bet.query.filter_by(creator_id=friend_two.user_to).all()

                for friend_two_bet in friend_two_bets:
                    # Get like count
                    count = models.Likes.query.filter_by(bet_id=friend_two_bet.id).count()

                    # Get if the current user liked the bet
                    like = models.Likes.query.filter_by(bet_id=friend_two_bet.id, user_id=user.id).count()

                    if like is 1:
                        liked = True
                    else:
                        liked = False

                    # Get users in bet
                    bet_users = models.BetUsers.query.filter_by(bet_id=friend_two_bet.id).all()
                    users = []

                    for bet_user in bet_users:
                        user = models.User.query.filter_by(id=bet_user.user_id).first()

                        users.append(user.toJSON)

                    # Make JSONobject
                    obj = friend_two_bet.toJSON

                    obj['numLikes'] = count
                    obj['liked'] = liked
                    obj['users'] = users

                    results.append(obj)

            response = jsonify({'bets': results})
            response.status_code = 200
            return response


######## My Open Bets ########
@betRoutes.route('/open', methods=['POST'])
def my_open_bets():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:

            bet_users = models.BetUsers.query.filter_by(user_id=user.id, active=1).all()
            results = []

            for bet_user in bet_users:

                bets = models.Bet.query.filter_by(id=bet_user.bet_id, complete=0).all()

                for bet in bets:

                    # Get like count
                    count = models.Likes.query.filter_by(bet_id=bet.id).count()

                    # Get if the current user liked the bet
                    like = models.Likes.query.filter_by(bet_id=bet.id, user_id=user.id).count()

                    if like is 1:
                        liked = True
                    else:
                        liked = False

                    # Get users in bet
                    bet_users = models.BetUsers.query.filter_by(bet_id=bet.id).all()
                    users = []

                    for bet_user in bet_users:
                        user = models.User.query.filter_by(id=bet_user.user_id).first()

                        users.append(user.toJSON)

                    # Make JSONobject
                    obj = bet.toJSON

                    obj['numLikes'] = count
                    obj['liked'] = liked
                    obj['users'] = users

                    results.append(obj)

            response = jsonify({'bets': results})
            response.status_code = 200
            return response


######## My Completed Bets ########
@betRoutes.route('/completed', methods=['POST'])
def my_completed_bets():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:

            bet_users = models.BetUsers.query.filter_by(user_id=user.id, active=1).all()
            results = []

            for bet_user in bet_users:

                bets = models.Bet.query.filter_by(id=bet_user.bet_id, complete=1).all()

                for bet in bets:

                    # Get like count
                    count = models.Likes.query.filter_by(bet_id=bet.id).count()

                    # Get if the current user liked the bet
                    like = models.Likes.query.filter_by(bet_id=bet.id, user_id=user.id).count()

                    if like is 1:
                        liked = True
                    else:
                        liked = False

                    # Get users in bet
                    bet_users = models.BetUsers.query.filter_by(bet_id=bet.id).all()
                    users = []

                    for bet_user in bet_users:
                        user = models.User.query.filter_by(id=bet_user.user_id).first()

                        users.append(user.toJSON)

                    # Make JSONobject
                    obj = bet.toJSON

                    obj['numLikes'] = count
                    obj['liked'] = liked
                    obj['users'] = users

                    results.append(obj)

            response = jsonify({'bets': results})
            response.status_code = 200
            return response


######## My Pending Bets ########
@betRoutes.route('/pending', methods=['POST'])
def my_pending_bets():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:

            bet_users = models.BetUsers.query.filter_by(user_id=user.id, active=0).all()
            results = []

            for bet_user in bet_users:

                bets = models.Bet.query.filter_by(id=bet_user.bet_id, complete=0).all()

                for bet in bets:

                    # Get like count
                    count = models.Likes.query.filter_by(bet_id=bet.id).count()


                    # Get if the current user liked the bet
                    like = models.Likes.query.filter_by(bet_id=bet.id, user_id=user.id).count()

                    if like is 1:
                        liked = True
                    else:
                        liked = False

                    # Get users in bet
                    bet_users = models.BetUsers.query.filter_by(bet_id=bet.id).all()
                    users = []

                    for bet_user in bet_users:
                        user = models.User.query.filter_by(id=bet_user.user_id).first()

                        users.append(user.toJSON)

                    # Make JSONobject
                    obj = bet.toJSON

                    obj['numLikes'] = count
                    obj['liked'] = liked
                    obj['users'] = users

                    results.append(obj)

            response = jsonify({'bets': results})
            response.status_code = 200
            return response


######## My Open Bets ########
@betRoutes.route('/bets/profile', methods=['POST'])
def profile():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:
            bet_users = models.BetUsers.query.filter_by(user_id=user.id)

            results = []

            for bet_user in bet_users:
                bet = models.Bet.query.filter_by(id=bet_user.bet_id).first()

                # Get like count
                count = models.Likes.query.filter_by(bet_id=bet.id).count()

                # Get if the current user liked the bet
                like = models.Likes.query.filter_by(bet_id=bet.id, user_id=user.id).count()

                if like is 1:
                    liked = True
                else:
                    liked = False

                # Get users in bet
                bet_users = models.BetUsers.query.filter_by(bet_id=bet.id).all()
                users = []

                for bet_user in bet_users:
                    user = models.User.query.filter_by(id=bet_user.user_id).first()

                    users.append(user.toJSON)

                # Make JSONobject
                obj = bet.toJSON

                obj['numLikes'] = count
                obj['liked'] = liked
                obj['users'] = users

                results.append(obj)

            response = jsonify({'bets': results})
            response.status_code = 200
            return response


######## Create Bet ########
@betRoutes.route('/bets/create', methods=['POST'])
def create_bet():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())

        # print(payload)

        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:

            creator = user.id
            maxUsers = payload['maxUsers']
            title = payload['title']
            description = payload['description']
            amount = payload['amount']
            locked = payload['locked']
            side_a = payload['sideA']
            side_b = payload['sideB']
            creation_time = datetime.datetime.now()

            try:
                bet = models.Bet(creator, maxUsers, title, description, amount, locked, side_a, side_b, creation_time)
            except AssertionError as e:
                return jsonify({'result': False, 'error': e.message}), 400

            bet.save()

            if transaction(user.id, bet.id, int(amount)) is False:
                db.session.delete(bet)
                db.session.commit()
                return jsonify({'result': False, 'error': 'Your balance is to low to create a bet'}), 400

            try:
                betUser = models.BetUsers(bet.id, creator, True, 0)
            except AssertionError as e:
                return jsonify({'result' : False, 'error': e.message}), 400
            betUser.save()
            return jsonify({'result': True, 'id': bet.id}), 200


######## Edit Bet ########
@betRoutes.route('/bets/update', methods=['POST'])
def edit_bet():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())

        print(payload)

        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:
            bet = models.Bet.query.filter_by(id=payload['betId']).first()

            if bet is None:
                return jsonify({'result': False, 'error': 'Bet does not exist'}), 400
            else:
                bet.creator = user.id
                bet.max_users = payload['maxUsers']
                bet.title = payload['title']
                bet.description = payload['description']
                bet.amount = payload['amount']
                bet.locked = payload['locked']
                bet.side_a = payload['sideA']
                bet.side_b = payload['sideB']

                try:
                    db.session.commit()
                except AssertionError as e:
                    return jsonify({'result': False, 'error': e.message}), 400

                return jsonify({'result': True, 'success': "Bet updated successfully"}), 200


######## Complete Bet ########
@betRoutes.route('/bets/complete', methods=['POST'])
def complete_bet():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Authenticate the token and extract values from the request
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    betID = payload['betID']
    winner = payload['winner']

    email = authClass.decode_jwt(token)
    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(models.User).filter_by(email=email).first()
    bet = db.session.query(models.Bet).filter_by(id=betID).first()

    if user is None:
        return jsonify({'result': False, 'error': 'User not found'}), 400

    if bet is None:
        return jsonify({'result': False, 'error': 'Bet not found'}), 400


    betUser = db.session.query(models.BetUsers).filter(and_(models.BetUsers.user_id == user.id,
                                                            models.BetUsers.bet_id == bet.id)).first()

    if betUser is None:
        return jsonify({'result': False, 'error': 'User not in the bet'}), 400

    firstComplete = False
    if betUser.confirmed is 2:
        firstComplete = True

    betUser.confirmed = winner
    betUser.save()

    # Find the betCreator

    betCreator = db.session.query(models.BetUsers).filter(and_(models.BetUsers.user_id == bet.creator_id,
                                                               models.BetUsers.bet_id == bet.id)).first()

    betUsers = db.session.query(models.BetUsers).filter_by(bet_id=bet.id).all()
    betUsersActive = []

    for user in betUsers:
        if user.active is 0:
            db.session.delete(user)
            db.session.commit()
        else:
            betUsersActive.append(user)

    return bet_completion(bet, winner)


def bet_completion(bet, winner):
    # Handle the transactions
    betUsers = db.session.query(models.BetUsers).filter_by(bet_id=bet.id).all()
    betWinners = db.session.query(models.BetUsers).filter(and_(models.BetUsers.bet_id == bet.id,
                                                               models.BetUsers.active == 1,
                                                               models.BetUsers.side == winner)).all()
    betLosers = db.session.query(models.BetUsers).filter(and_(models.BetUsers.bet_id == bet.id,
                                                               models.BetUsers.active == 1,
                                                               models.BetUsers.side != winner)).all()

    numOfWinners = len(betWinners)
    # Delete all users that did not accept invites and get the total count of users
    for user in betUsers:
        if user.active == 0:
            db.session.delete(user)
            db.session.commit()

    if numOfWinners != 0:
        amount = bet.pot // numOfWinners
    else:
        amount = -bet.amount

    for user in betWinners:
        if transaction(user.user_id, bet.id, -amount) is False:
            return jsonify({'result': False, 'error': 'Transaction error'}), 400

    bet.complete = 1
    bet.locked = 1
    bet.winner = winner
    bet.save()

    # Query for all active users in the bet
    betUsersActive = db.session.query(models.BetUsers).filter(and_(models.BetUsers.bet_id == bet.id,
                                                                   models.BetUsers.active == 1)).all()

    # Send bet completion notifications
    title = bet.title + " has been completed"
    message = "The winning side is " + bet.side_b if winner else "The winning side is " + bet.side_a
    return jsonify({'result': True, 'error': ""}), 200
    #return bet_notification(betUsersActive, title, message)
