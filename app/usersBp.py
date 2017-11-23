from flask import Blueprint, json, request, jsonify, render_template

from pyfcm import FCMNotification

userRoutes = Blueprint('users', __name__)

from .authRoutines import *
from .models import *
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
    email = payload['email']

    if authClass.decode_jwt(token) is False:
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


@userRoutes.route('/users/notifyAll', methods=['GET'])
def notifyAll():
    push_service = FCMNotification(api_key="AAAA2-UdK4Y:APA91bGo5arWnYhVRofMxAaaM9XXHijNQxxqSw5GsLkEyNMqe1ITIyJSRXQ51Hwr7985E1bLYH_y-VqRzMPC5b_J3QGRpRdWBgGNZXb17Io0bsHxOJe0qoAwekuKd0901YcgeLTR_kkE")

    registration_id = "fBvbHdhYNd4:APA91bE_spuZqv94zeCCJ-Bsgp88pO1hjV3I6uqmB-MRentD03DLD5kX5LrpkGXSn0qW8e1m6UuQcyqIqoe4w6HMHCTE-hY6uUNWpBN7nwcGwejAtAHlYbzYPnHt4yWMox4catr9Zcsf"
    message_title = "TEST"
    message_body = "HI THIS IS A TEST"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                               message_body=message_body)

    return jsonify({'result': True, 'error': ''}), 200


@userRoutes.route('/users/updateDevice', methods=['POST'])
def updateDeivce():
    authClass = authBackend()

    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']

        email = authClass.decode_jwt(token)

        user = db.session.query(User).filter_by(email=email).first()

        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400
        else:
            user.device_id = payload['deviceId']

            try:
                user.save()
                return jsonify({'result': True, 'error': ''}), 200
            except:
                return jsonify({'result': False, 'error': 'Failed to save deviceId'}), 400


@userRoutes.route('/admin', methods=['GET'])
def displayAdmin():
    feedbacks = [
        {
            "email": "yopickles",
            "text": "This app freaking sucks"
        },
        {
            "email": "notpickles",
            "text": "I love you all :D"
        }
    ]
    return render_template("admin.html", feedbacks=feedbacks)