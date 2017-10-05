from jose import jwt
import datetime

    from app.config import Config

from google.oauth2 import id_token
from google.auth.transport import requests

class authBackend:

    def __init__(self, userid = None):
        self.userid = None
        self.CLIENT_ID = Config.GOOGLE_CLIENT_KEY
        self.JWT_KEY = Config.JWT_KEY

    def setUserId(self, userid):
        self.userid = userid

    def generateNewToken(self):
        newToken = jwt.encode({'user' : self.userid, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4)}, self.JWT_KEY, algorithm='HS256')
        return newToken

    def google_check(token):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise ValueError('Wrong issuer.')
            userid = idinfo['sub']
            return userid
        except ValueError:
		    # Invalid token
			return False

    def decode_jwt(self, jwt):
        try:
            decodeToken = jwt.decode(jwt, self.JWT_KEY, algorithms = 'HS256')
            return decodeToken['user']
        except jwt.ExpiredSignatureError:
            try:
                getUsername = jwt.decode(jwt, self.JWT_KEY, algorithms = 'HS256', options = {'verify_exp' : False})
                return getUsername['user']
            except:
                return False
        except:
            return False
