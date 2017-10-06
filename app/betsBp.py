from flask import request, jsonify, abort, Blueprint

import requests
import json
from app import models
from app import authRoutines

betRoutes = Blueprint('betsBp', __name__)


@betRoutes.route('/publicfeed', methods=['GET'])
def public_feed():
    # GET
    bets = models.Bet.get_all()
    results = []

    for bet in bets:
        obj = {
            'id': bet.id,
            'max_users': bet.max_users,
            'title': bet.title,
            'text': bet.text,
            'amount': bet.amount,
            'completed': bet.completed
        }
        results.append(obj)

    response = jsonify({'bets': results})
    response.status_code = 200
    return response


@betRoutes.route('/mybets/<int:user_id>', methods=['POST'])
def my_bets(user_id):

    authClass = authRoutines.authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        if authClass.decode_jwt(token) is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:
            bets = models.Bet.query.filter(models.Bet.creator_id == user_id)
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

            response = jsonify({'bets': results})
            response.status_code = 200
            return response