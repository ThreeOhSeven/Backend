from flask import request, jsonify, abort, Blueprint

import requests
import json
from app import models
from .authRoutines import *

commentRoutes = Blueprint('commentBp', __name__)


# {authToken: xxxx, betId: xxxx, text: xxxx}
@commentRoutes.route('/comment/add', methods=['POST'])
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

    creator_id = models.Bet.query.filter_by(id=bet_id).first().creator_id

    if user.id != creator_id:
        if not (models.Friend.query.filter_by(friend_to=user.id, friend_from=creator_id).first() or models.Friend.query.filter_by(friend_to=creator_id, friend_from=user.id).first()):
            return jsonify({'result': True, 'error': 'User not friend of owner'}), 400

    if len(text) > 280:
        return jsonify({'result': True, 'error': 'Comment was too long'}), 400

    comment = models.Comment(user.id, bet_id, text)

    try:
        comment.save()
        return jsonify({'result': True, 'success': 'Comment Created'}), 200
    except:
        return jsonify({'result': True, 'error': 'Comment Failed to save'}), 400


# {authToken: xxxx, commentId: xxxx}
@commentRoutes.route('/comment/delete', methods=['POST'])
def delete_comment():
    authClass = authBackend()

    if request.method != 'POST':
        return jsonify({'result': False, 'error': 'Only POST accepted'}), 400

    payload = json.loads(request.data.decode())
    token = payload['authToken']

    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(models.User).filter_by(email=email).first()

    comment = models.Comment.query.filter_by(id=payload['commentId']).first()

    if comment.user_id != user.id:
        return jsonify({'result': False, 'error': 'Not owner of comment'}), 400

    try:
        comment.delete()
    except:
        return jsonify({'result': False, 'error': 'Failed to delete comment'}), 400

    return jsonify({'result': True, 'success': 'Comment Deleted'}), 200


# {authToken: xxxx, commentId: xxxx}
@commentRoutes.route('/comment/get', methods=['POST'])
def get_comments():
    authClass = authBackend()

    if request.method != 'POST':
        return jsonify({'result': False, 'error': 'Only POST accepted'}), 400

    payload = json.loads(request.data.decode())
    token = payload['authToken']

    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(models.User).filter_by(email=email).first()

    comments = models.Comment.query.filter_by(bet_id=payload['betId']).all()

    result = []

    for comment in comments:
        result.append(comment.toJSON)

    response = jsonify({'comments': result})
    response.status_code = 200
    return response
