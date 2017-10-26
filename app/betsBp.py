from flask import request, jsonify, abort, Blueprint

import requests
import json
from app import models
from .authRoutines import *

betRoutes = Blueprint('betsBp', __name__)


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
                print(count)

                # Get if the current user liked the bet
                like = models.Likes.query.filter_by(bet_id=bet.id, user_id=user.id).count()


                if count is 1:
                    liked = True
                else:
                    liked = False

                print(liked)

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


@betRoutes.route('/mybets', methods=['POST'])
def my_bets():

    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()


        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:


            bets = db.session.query(models.Bet).filter_by(creator_id=user.id)
            results = []

            for bet in bets:
                obj = {
                    'id': bet.id,
                    'creator': bet.creator_id,
                    'max_users': bet.max_users,
                    'title': bet.title,
                    'description': bet.text,
                    'amount': bet.amount,
                    'winner': 'Test',
                    'locked': bet.locked
                }
                results.append(obj)


            response = jsonify({'myBets': results})
            response.status_code = 200
            return response


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

