from flask import Blueprint, json, request, jsonify

userRoutes = Blueprint('users', __name__)

from .authRoutines import *
authClass = authBackend()

@userRoutes.route('/info', methods=['POST'])
def getInfo():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query the user table based on the email
    user = db.session.query(User).filter_by(email=email).first()

    if user is None:
        return jsonify({'result': False, 'error': "User does not exist"}), 400

    return jsonify({'result': True, 'error': "",
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'birthday': user.birthday}), 200


@userRoutes.route('/edit', methods=['POST'])
def editInfo():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query the user table based on the email
    user = db.session.query(User).filter_by(email=email).first()

    if user is None:
        return jsonify({'result': False, 'error': "User does not exist"}), 400

    user = db.session.query(User).filter_by(id=user.id).first()

    account_info = payload['accountInformation']
    user.username = account_info['username']
    #user.email = account_info['email']
    user.birthday = account_info['birthday']
    db.session.commit()

    return jsonify({'result': True, 'error': ''}), 200


@userRoutes.route('/delete', methods=['POST'])
def deleteUser():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query the user table based on the email
    user = db.session.query(User).filter_by(email=email).first()

    if user is None:
        return jsonify({'result': False, 'error': 'User does not exist'}), 400

    db.session.delete(user)
    db.session.commit()

    return jsonify({'result': True, 'error': ''}), 200

@userRoutes.route('/users/get/id', methods=['POST'])
def getIdByEmail():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query the user table based on the email
    user = db.session.query(User).filter_by(email=email).first()

    if user is None:
        return jsonify({'resuslt': True, 'error': ''}), 400

    return jsonify({'result': True, 'error': '', 'id': user.id}), 200

@userRoutes.route('/users/get/email', methods=['POST'])
def getEmailById():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's token from 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    id = payload['id']

    if authClass.decode_jwt(token) is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query the user table based on the id provided
    user = db.session.query(User).filter_by(id=id).first()

    if user is None:
        return jsonify({'resuslt': True, 'error': ''}), 400

    return jsonify({'result': True, 'error': '', 'email': user.email}), 200

