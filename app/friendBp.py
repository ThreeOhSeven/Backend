from flask import Blueprint, json, request, jsonify
import requests
from sqlalchemy import or_, and_
from app import db
from .models import User, Friend

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

    id = user.id

    # Query both columns to find all friend pairs containing the given id
    friends_to = db.session.query(Friend).filter_by(user_to=id).all()
    friends_from = db.session.query(Friend).filter_by(user_from=id).all()

    friends = friends_to + friends_from

    # Create and format a list of friends to send as a response
    results = []
    for friend in friends:
        if friend.user_to == id:
            user = db.session.query(User).filter_by(id=friend.user_from).first()
        else:
            user = db.session.query(User).filter_by(id=friend.user_to).first()

        if user is None:
            return jsonify({'result': False, 'error': 'User not found'}), 400

        obj = {
            'status': friend.status,
            'friend': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'birthday': user.birthday
            }
        }
        results.append(obj)
    return jsonify({'friends_obj': results}), 200

@friendsRoutes.route('/add/<id>', methods=['POST'])
def addFriend(id):
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query for both users using the email from the token and the given id
    user_to = db.session.query(User).filter_by(id=int(id)).first()
    user_from = db.session.query(User).filter_by(email=email).first()

    if user_to is None or user_from is None:
        return jsonify({'result': False, 'error': 'One or more user not found in the database'}), 400

    if user_to == user_from:
        return jsonify({'result': False, 'error': 'User cannot add themselves'}), 400

    # Only store friendPairs with user_to: lower id, user_from: higher id
    if user_to.id > user_from.id:
        swap = user_to
        user_to = user_from
        user_from = swap

    # Query for the friendship
    friendship = db.session.query(Friend).filter(and_(Friend.user_to == user_to.id,
                                                      Friend.user_from == user_from.id)).first()

    # Perform different tasks based on friendship status
    if friendship is None:
        new_friendship = Friend(user_to.id, user_from.id, 0)
        db.session.add(new_friendship)
        db.session.commit()
        return jsonify({'result': True, 'error': ''}), 200
    elif friendship.status == 1:
        return jsonify({'result': False, 'error': 'Users are already friends'})
    elif friendship.status == 0:
        friendship.status = 1
        db.session.commit()

    return jsonify({'result': True, 'error': ''}), 200


@friendsRoutes.route('/delete/<id>', methods=['POST'])
def deleteFriend(id):
    if request.method != 'POST':
        return jsonify({'result': False, 'error': "Invalid request"}), 400

    # Get the user's email based on the 'authToken'
    payload = json.loads(request.data.decode())
    token = payload['authToken']
    email = authClass.decode_jwt(token)

    if email is False:
        return jsonify({'result': False, 'error': 'Failed Token'}), 400

    # Query for both users using the email from the token and the given id
    user_to = db.session.query(User).filter_by(id=int(id)).first()
    user_from = db.session.query(User).filter_by(email=email).first()

    if user_to is None or user_from is None:
        return jsonify({'result': False, 'error': 'One or more user not found in the database'}), 400

    if user_to == user_from:
        return jsonify({'result': False, 'error': 'User cannot add themselves'}), 400

    # Only store friendPairs with user_to: lower id, user_from: higher id
    if user_to.id > user_from.id:
        swap = user_to
        user_to = user_from
        user_from = swap

    # Query for the friendship
    friendship = db.session.query(Friend).filter(and_(Friend.user_to == user_to.id,
                                                      Friend.user_from == user_from.id)).first()

    if friendship is None:
        return jsonify({'result': False, 'error': 'Friendship does not exist'}), 400

    db.session.delete(friendship)
    db.session.commit()

    return jsonify({'result': True, 'error': ''}), 200
