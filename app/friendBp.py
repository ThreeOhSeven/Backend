from flask import Blueprint, json, request, jsonify
import requests
from sqlalchemy import or_, and_
from app import db
from pyfcm import FCMNotification
#from .models import User, Friend

friendsRoutes = Blueprint('friends', __name__)
from .authBp import authBackend

authClass = authBackend()

@friendsRoutes.route('/', methods=['POST'])
def getFriends():
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
        return jsonify({'result': False, 'error': 'User not found'}), 400

    # Query both columns to find all friend pairs containing the given id
    friends_from = db.session.query(Friend).filter_by(user_from=user.id).all()
    friends_to = db.session.query(Friend).filter_by(user_to=user.id).all()

    friends = friends_from + friends_to

    # Create and format a list of friends to send as a response
    results = []
    for friendship in friends:
        if friendship.status == 1:
            friend = db.session.query(User).filter_by(id=friendship.user_from).first() \
                if friendship.user_to == user.id else db.session.query(User).filter_by(id=friendship.user_to).first()
            obj = {
                'status': friendship.status,
                'friend':
                {
                    'id': friend.id,
                    'username': friend.username,
                    'email': friend.email,
                    'birthday': friend.birthday
                }
            }
            results.append(obj)

    return jsonify({'friends_obj': results}), 200

@friendsRoutes.route('/pending', methods=['POST'])
def getPending():
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
        return jsonify({'result': False, 'error': 'User not found'}), 400

    # Query both columns to find all friend pairs containing the given id
    friendRequests = db.session.query(Friend).filter(and_(Friend.user_from == user.id, Friend.status == 0)).all()

    # Create and format a list of friends to send as a response
    results = []
    for friendRequest in friendRequests:
        friend = db.session.query(User).filter_by(id=friendRequest.user_to).first()
        obj = {
            'status': friendRequest.status,
            'friend':
            {
                'id': friend.id,
                'username': friend.username,
                'email': friend.email,
                'birthday': friend.birthday
             }
         }
        results.append(obj)

    return jsonify({'friends_obj': results}), 200


@friendsRoutes.route('/requests', methods=['POST'])
def getRequests():
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
        return jsonify({'result': False, 'error': 'User not found'}), 400

    # Query both columns to find all friend pairs containing the given id
    friendRequests = db.session.query(Friend).filter(and_(Friend.user_to == user.id, Friend.status == 0)).all()

    # Create and format a list of friends to send as a response
    results = []
    for friendRequest in friendRequests:
        friend = db.session.query(User).filter_by(id=friendRequest.user_from).first()
        obj = {
            'status': friendRequest.status,
            'friend':
                {
                    'id': friend.id,
                    'username': friend.username,
                    'email': friend.email,
                    'birthday': friend.birthday
                }
        }
        results.append(obj)

    return jsonify({'friends_obj': results}), 200

@friendsRoutes.route('/add/', methods=['POST'])
def addFriend():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    id = payload['id']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query for both users using the email from the token and the given id
    user_from = db.session.query(User).filter_by(email=email).first()
    user_to = db.session.query(User).filter_by(id=id).first()

    if user_from is None or user_to is None:
        return jsonify({'result': False, 'error': 'One or more user not found in the database'}), 400

    if user_from == user_to:
        return jsonify({'result': False, 'error': 'User cannot add themselves'}), 400

    # Query for the friendship
    friendship = db.session.query(Friend).filter(and_(Friend.user_from == user_from.id,
                                                      Friend.user_to == user_to.id)).first()
    friendshipReverse = db.session.query(Friend).filter(and_(Friend.user_from == user_to.id,
                                                      Friend.user_to == user_from.id)).first()

    friendship = friendship if friendship is not None else friendshipReverse

    # Perform different tasks based on friendship status
    if friendship is None:
        new_friendship = Friend(user_to.id, user_from.id, 0)
        db.session.add(new_friendship)
        db.session.commit()

        if user_to.device_id:
            # Notify User
            push_service = FCMNotification(
                api_key="AAAA2-UdK4Y:APA91bGo5arWnYhVRofMxAaaM9XXHijNQxxqSw5GsLkEyNMqe1ITIyJSRXQ51Hwr7985E1bLYH_y-VqRzMPC5b_J3QGRpRdWBgGNZXb17Io0bsHxOJe0qoAwekuKd0901YcgeLTR_kkE")

            registration_id = user_to.device_id
            message_title = "Friend Request"
            message_body = user_from.email + " has sent you a friend request"
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)

        return jsonify({'result': True, 'error': ''}), 200
    elif friendship.status == 1:
        return jsonify({'result': False, 'error': 'Users are already friends'}), 400
    elif friendship.status == 0:
        # Check to see if the calling user is a requester or requestee
        # if requester, tell them the friend request is still pending
        if friendship.user_to == user_from.id:
            friendship.status = 1
            db.session.commit()
        else:
            return jsonify({'result': False, 'error': 'The friend request is still pending'}), 400

    return jsonify({'result': True, 'error': ''}), 200


@friendsRoutes.route('/delete/', methods=['POST'])
def deleteFriend():
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    id = payload['id']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query for both users using the email from the token and the given id
    user_from = db.session.query(User).filter_by(email=email).first()
    user_to = db.session.query(User).filter_by(id=id).first()

    if user_from is None or user_to is None:
        return jsonify({'result': False, 'error': 'One or more user not found in the database'}), 400

    if user_from == user_to:
        return jsonify({'result': False, 'error': 'User cannot add themselves'}), 400

    # Query for the friendship
    friendship = db.session.query(Friend).filter(and_(Friend.user_from == user_from.id,
                                                      Friend.user_to == user_to.id)).first()
    friendshipReverse = db.session.query(Friend).filter(and_(Friend.user_from == user_to.id,
                                                             Friend.user_to == user_from.id)).first()

    friendship = friendship if friendship is not None else friendshipReverse

    if friendship is None:
        return jsonify({'result': False, 'error': 'Friendship does not exist'}), 400

    db.session.delete(friendship)
    db.session.commit()

    return jsonify({'result': True, 'error': ''}), 200
