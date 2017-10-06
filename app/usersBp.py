from flask import Blueprint, json, request, jsonify
import requests

from app import db
from .models import User

userRoutes = Blueprint('users', __name__)

from .authRoutines import *
authClass = authBackend()

@userRoutes.route('/create', methods=['POST'])
def createUser():
    if request.method == 'POST':
        payload = request.get_json(force=True)
        token = payload['authToken']
        if authClass.decode_jwt(token) is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        username = payload['username']
        email = payload['email']
        birthday = payload['birthday']
        try:
            user = User(username, email, birthday)
        except AssertionError as e:
            return jsonify({'result': False, 'error': e.message}), 400
        db.session.add(user)
        db.session.commit()
        return jsonify({'result': True, 'error': ""}), 200
    return jsonify({'result': False, 'error': "Invalid request"}), 400

@userRoutes.route('/info', methods=['POST'])
def getInfo():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400

        user = db.session.query(User).filter_by(email=email).first()
        if user is None:
            return jsonify({'result': False, 'error': "User does not exist"}), 400
        return jsonify({'result': True, 'error': "",
                        'username': user.username,
                        'email': user.email,
                        'birthday': user.birthday}), 200
    return jsonify({'result': False, 'error': "Invalid request"}), 400

@userRoutes.route('/edit', methods=['POST'])
def editInfo():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        if authClass.decode_jwt(token) is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        accountInfo = payload['accountInformation']
        user = db.session.query(User).filter_by(id=accountInfo['id']).first()
        try:
            user.username = accountInfo['username']
            user.email = accountInfo['email']
            user.birthday = accountInfo['birthday']
            db.session.commit()
        except AssertionError as e:
            return jsonify({'result': False, 'error': e.message}), 400
        return jsonify({'result': True, 'error': ''}), 200
    return jsonify({'result': False, 'error': "Invalid request"}), 400

@userRoutes.route('/delete', methods=['POST'])
def deleteUser():
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        user = db.session.query(User).filter_by(email=email).first()
        if user is None:
            return jsonify({'result': False, 'error': 'User does not exist'}), 400
        db.session.delete(user)
        db.session.commit()
        return jsonify({'result': True, 'error': ''}), 200
    return jsonify({'result': False, 'error': "Invalid request"}), 400
