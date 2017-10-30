from flask import request, jsonify, abort, Blueprint

import requests
import json
from app import models
from .authRoutines import *

betRoutes = Blueprint('betsBp', __name__)


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

                obj['num_likes'] = count
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

                # Make JSONObject to return
                obj = {
                    'id': bet.id,
                    'creator_id': bet.creator_id,
                    'max_users': bet.max_users,
                    'title': bet.title,
                    'description': bet.description,
                    'amount': bet.amount,
                    'winner': bet.winner,
                    'locked': bet.locked,
                    'complete': bet.complete,
                    'num_likes': count,
                    'liked': liked
                }
                results.append(obj)

            # Friends Side 1
            friends_one = models.Friend.query.filter_by(user_to=user.id, status=1).all()

            for friend_one in friends_one:
                friend_one_bets = models.Bet.query.filter_by(user_id=friend_one.user_from).all()

                for friend_one_bet in friend_one_bets:
                    # Get like count
                    count = models.Likes.query.filter_by(bet_id=friend_one_bet.id).count()

                    # Get if the current user liked the bet
                    like = models.Likes.query.filter_by(bet_id=friend_one_bet.id, user_id=user.id).count()

                    if like is 1:
                        liked = True
                    else:
                        liked = False

                    # Make JSONObject to return
                    obj = {
                        'id': bet.id,
                        'creator_id': bet.creator_id,
                        'max_users': bet.max_users,
                        'title': bet.title,
                        'description': bet.description,
                        'amount': bet.amount,
                        'winner': bet.winner,
                        'locked': bet.locked,
                        'complete': bet.complete,
                        'num_likes': count,
                        'liked': liked
                    }
                    results.append(obj)

            # Friends Side 2
            friends_two = models.Friend.query.filter_by(user_from=user.id, status=1).all()

            for friend_two in friends_two:
                friend_two_bets = models.Bet.query.filter_by(user_id=friend_two.user_to).all()

                for friend_two_bet in friend_two_bets:
                    # Get like count
                    count = models.Likes.query.filter_by(bet_id=friend_two_bet.id).count()

                    # Get if the current user liked the bet
                    like = models.Likes.query.filter_by(bet_id=friend_two_bet.id, user_id=user.id).count()

                    if like is 1:
                        liked = True
                    else:
                        liked = False

                    # Make JSONObject to return
                    obj = {
                        'id': bet.id,
                        'creator_id': bet.creator_id,
                        'max_users': bet.max_users,
                        'title': bet.title,
                        'description': bet.description,
                        'amount': bet.amount,
                        'winner': bet.winner,
                        'locked': bet.locked,
                        'complete': bet.complete,
                        'num_likes': count,
                        'liked': liked
                    }
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

                    # Make JSONObject to return
                    obj = {
                        'id': bet.id,
                        'creator_id': bet.creator_id,
                        'max_users': bet.max_users,
                        'title': bet.title,
                        'description': bet.description,
                        'amount': bet.amount,
                        'winner': bet.winner,
                        'locked': bet.locked,
                        'complete': bet.complete,
                        'num_likes': count,
                        'liked': liked
                    }
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


                    # Make JSONObject to return
                    obj = {
                        'id': bet.id,
                        'creator_id': bet.creator_id,
                        'max_users': bet.max_users,
                        'title': bet.title,
                        'description': bet.description,
                        'amount': bet.amount,
                        'winner': bet.winner,
                        'locked': bet.locked,
                        'complete': bet.complete,
                        'num_likes': count,
                        'liked': liked
                    }
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


                    # Make JSONObject to return
                    obj = {
                        'id': bet.id,
                        'creator_id': bet.creator_id,
                        'max_users': bet.max_users,
                        'title': bet.title,
                        'description': bet.description,
                        'amount': bet.amount,
                        'winner': bet.winner,
                        'locked': bet.locked,
                        'complete': bet.complete,
                        'num_likes': count,
                        'liked': liked
                    }
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

        print(payload)

        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:

            creator = user.id
            maxUsers = payload['maxUsers']
            title = payload['title']
            text = payload['description']
            amount = payload['amount']
            locked = payload['locked']


            try:
                bet = models.Bet(creator, maxUsers, title, text, amount, locked)
            except AssertionError as e:
                return jsonify({'result': False, 'error': e.message}), 400
            bet.save()
            return jsonify({'result': True, 'error': ""}), 200


######## Edit Bet ########
@betRoutes.route('/bets/edit', methods=['POST'])
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
            bet = models.Bet.query.filter_by(bet_id=payload['betId']).first()

            if bet is None:
                return jsonify({'result': False, 'error': 'Bet does not exist'}), 400
            else:
                bet.creator = user.id
                bet.maxUsers = payload['maxUsers']
                bet.title = payload['title']
                bet.text = payload['description']
                bet.amount = payload['amount']
                bet.locked = payload['locked']

                try:
                    db.session.commit()
                except AssertionError as e:
                    return jsonify({'result': False, 'error': e.message}), 400

                return jsonify({'result': True, 'success': "Bet updated successfully"}), 200


######## Join Bet ########
@betRoutes.route('/bets/join', methods=['POST'])
def join_bet():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:
            bet_id = payload['betId']

            betUser = models.BetUsers(bet_id=bet_id, user_id=user.id)

            betUser.save()



