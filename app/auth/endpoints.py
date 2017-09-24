from flask import Blueprint, session, jsonify, request, render_template, session
import requests
import json

from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = "944441731974-cps00fl7ob138hknau1ceqo5pgu8ad2m.apps.googleusercontent.com"
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
		# try:
		idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
		print(idinfo)
	    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
	    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
	    #     raise ValueError('Could not verify audience.')
		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
			raise ValueError('Wrong issuer.')

	    # ID token is valid. Get the user's Google Account ID from the decoded token.
		userid = idinfo['sub']
		return jsonify({'result' : True, 'selfToken' : "askdjaksdjqoiwuoqiuwjkleaksd"})
		# except ValueError:
		    # Invalid token
			# return jsonify({'result' : False, 'error' : "Invalid token"})
	return jsonify({'result' : False, 'error' : "Invalid request"})
