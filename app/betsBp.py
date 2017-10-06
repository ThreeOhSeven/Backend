from flask import request, jsonify, abort, Blueprint

import requests
import json
from app import models

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

@betRoutes.route('/mybets', methods=['POST'])
def my_bets():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']