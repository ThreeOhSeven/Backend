from flask import request, jsonify, abort, Blueprint

import requests
import json
from app.models import Notification
from .authRoutines import *

class Notifications:


    def add_notification(user_id, title, message):

        notification = Notification(user_id, title, message).save()

        # TODO - Send notification to user