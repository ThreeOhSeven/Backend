from flask import request, jsonify, abort, Blueprint

import requests
import json
from app.models import Notification
from .authRoutines import *
from pyfcm import FCMNotification

api_key = "AAAA2-UdK4Y:APA91bGo5arWnYhVRofMxAaaM9XXHijNQxxqSw5GsLkEyNMqe1ITIyJSRXQ51Hwr7985E1bLYH_y-VqRzMPC5b_J3QGRpRdWBgGNZXb17Io0bsHxOJe0qoAwekuKd0901YcgeLTR_kkE"


class Notifications:

    @staticmethod
    def create_notification(user_id, title, message):

        notification = Notification(user_id, title, message)
        notification.save()

        temp_user = User.query.filter_by(id=user_id).first()

        if temp_user.device_id:
            # Notify User
            push_service = FCMNotification(api_key)

            registration_id = temp_user.device_id
            message_title = title
            message_body = message
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)
