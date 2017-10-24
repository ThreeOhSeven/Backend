from flask import request, jsonify, abort, Blueprint

import requests
import json
from app import models
from .authRoutines import *

likeRoutes = Blueprint('likesBp', __name__)


# {authToken: xxxx, like: 0, betId: xxxx}
# {authToken: xxxx, like: 1, betId: xxxx}
@likeRoutes.route('/like/update', methods=['POST'])
def like_update():
    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(models.User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:
            bet = db.session.query(models.Bet).filter_by(id=payload['betId']).first()

            if bet is None:
                return jsonify({'result': False, 'error': 'Bet Doesn\'t Exist'}), 400
            else:
                like = db.session.query(models.Likes).filter_by(user_id=user.id, bet_id=bet.id).first()

                if payload['like'] == 1:

                    if like is None:
                        like = models.Likes(bet.id, user.id)
                        like.save()

                        return jsonify({'result': True, 'success': 'Like Created'}), 200
                else:

                    if like is not None:
                        db.session.delete(like)

                        return jsonify({'result': True, 'success': 'Like Removed'}), 200
