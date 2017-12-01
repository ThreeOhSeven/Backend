from flask import request, jsonify, abort, Blueprint

import requests
import json
from app.models import Notification
from .authRoutines import *
from app import notifications

notificationRoutes = Blueprint('notificationBp', __name__)


# {authToken: xxxx, userId: xxxx}
@notificationRoutes.route('/get', methods=['POST'])
def get_notifications():
    authClass = authBackend()

    if request.method != 'POST':
        return jsonify({'result': False, 'error': 'Only POST accepted'}), 400

    payload = json.loads(request.data.decode())
    token = payload['authToken']

    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    user = db.session.query(User).filter_by(email=email).first()

    notification_feed = Notification.query.filter_by(user_id=user.id).all()

    res = []

    for notification in notification_feed:
        res.append(notification.toJSON)

        notification.viewed = True
