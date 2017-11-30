from flask import request, jsonify, abort, Blueprint

import requests
import json
from app.models import Notification
from .authRoutines import *

notifcationRoutes = Blueprint('notificationBp', __name__)


# {authToken: xxxx, userId: xxxx}
@notifcationRoutes.route('/notifications/get', methods=['POST'])
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

    notifications = Notification.query.filter_by(user_id=user.id).all()


def add_notification(user_id, title, message):

    notification = Notification(user_id, title, message).save()