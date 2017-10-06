from flask import Blueprint, session, jsonify, request, render_template, session
import requests
import json

from app import db
from .models import User

from .authRoutines import *

authRoutes = Blueprint('authBp', __name__)

@authRoutes.route("/")
def index():
	return "hello world"

@authRoutes.route("/auth/login", methods = ["POST"])
def checkLogin():
	# (Receive token by HTTPS POST)
	# ...
	if request.method == 'POST':
		payload = json.loads(request.data.decode())
		token = payload['authToken']
		authClass = authBackend()
		userId = authClass.google_check(token)
		if not userId:
			return jsonify({'result' : False, 'error' : "Invalid token"})
		authClass.setUserId(userId)
		userExist = authClass.check_self_email(userId)
		if not userExist:
			addSuc = authClass.create_new_user(userId)
			if not addSuc:
				print("user not added")
		newToken = authClass.generateNewToken()
		username = None
		email = payload['email']
		birthday = None
		try:
			user = User(username, email, birthday)
		except AssertionError as e:
			return jsonify({'result': False, 'error': e.message}), 400
		db.session.add(user)
		db.session.commit()

		return jsonify({'result' : True, 'selfToken' : newToken})
	return jsonify({'result' : False, 'error' : "Invalid request"})
