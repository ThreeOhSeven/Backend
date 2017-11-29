from flask import request, jsonify, abort, Blueprint

import requests
import json
from app import models
from .authRoutines import *

commentRoutes = Blueprint('commentBp', __name__)


# {authToken: xxxx, betId: xxxx, text: xxxx}
@commentRoutes.route('/comment', methods=['POST'])
def add_comment():
    authClass = authBackend()

    if request.method != 'POST':
        return jsonify({'result': False, 'error': 'Only POST accepted'}), 400

    payload = json.loads(request.data.decode())
    token = payload['authToken']

    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(models.User).filter_by(email=email).first()

    bet_id = payload["betId"]
    text = payload["text"]

    comment = models.Comment(user.id, bet_id, text)

    try:
        comment.save()
    except:
        return jsonify({'result': True, 'success': 'Comment Created'}), 200
