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
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400

        user = db.session.query(User).filter_by(email=email).first()

        if user is None:
            return jsonify({'result': False, 'error': 'User not found'}), 400

        # friends = db.session.query(Friend).filter(or_(Friend.user_to == id, Friend.user_from == id))


        id = user.id
        print("Here")

        friends_to = db.session.query(Friend).filter_by(user_to=id).all()
        friends_from = db.session.query(Friend).filter_by(user_from=id).all()


        friends = friends_to + friends_from

        results = []
        for friend in friends:
            obj = {
                'status': friend.status,
                'user_to': friend.user_to,
                'user_from': friend.user_from
            }
            results.append(obj)
        response = jsonify(results), 200
        return response

    return jsonify({'result': False, 'error': "Invalid request"}), 400

@friendsRoutes.route('/add/<id>', methods=['POST'])
def addFriend(id):
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400

        from_id = db.session.query(User).filter_by(email=email).first()

        if from_id is None:
            return jsonify({'result': False, 'error': 'User not found'}), 400

        to_id = int(id)

        if to_id == from_id:
            return jsonify({'result': False, 'error': 'User cannot add themselves'}), 400

        user_to = db.session.query(User).filter_by(id=to_id).first()
        user_from = db.session.query(User).filter_by(id=from_id.id).first()

        if user_to is None or user_from is None:
            return jsonify({'result': False, 'error': 'One or more user not found in the database'}), 400

        friendship = db.session.query(Friend).filter(and_(Friend.user_to == user_to.id,
                                                         Friend.user_from == user_from.id)).first()

        if friendship is None:
            newFriendship = Friend(user_to.id, user_from.id, 0)
            db.session.add(newFriendship)
            db.session.commit()
            return jsonify({'result': True, 'error': ''}), 200
        elif friendship.status == 1:
            return jsonify({'result': False, 'error': 'Users are already friends'})
        elif friendship.status == 0:
            friendship.status = 1
            db.session.commit()

        return jsonify({'result': True, 'error': ''}), 200
    return jsonify({'result': False, 'error': "Invalid request"}), 400

@friendsRoutes.route('/delete/<id>', methods=['POST'])
def deleteFriend(id):
    if request.method == 'POST':
        payload = json.loads(request.data.decode())
        token = payload['authToken']
        email = authClass.decode_jwt(token)
        if email is False:
            return jsonify({'result': False, 'error': 'Failed Token'}), 400

        from_id = db.session.query(User).filter_by(email=email).first()
        if from_id is None:
            return jsonify({'result': False, 'error': 'User not found'}), 400

        to_id = int(id)

        user_to = db.session.query(User).filter_by(id=to_id).first()
        user_from = db.session.query(User).filter_by(id=from_id.id).first()

        if user_to is None or user_from is None:
            return jsonify({'result': False, 'error': 'One or more user not found in the database'}), 400

        friendship = db.session.query(Friend).filter(and_(Friend.user_to == user_to.id,
                                                          Friend.user_from == user_from.id)).first()
        reverseFriendship = db.session.query(Friend).filter(and_(Friend.user_to == user_from.id,
                                                          Friend.user_from == user_to.id)).first()


        friendship = friendship if friendship is not None else reverseFriendship

        if friendship is None:
            return jsonify({'result': False, 'error': 'Friendship does not exist'}), 400

        db.session.delete(friendship)
        db.session.commit()

        return jsonify({'result': True, 'error': ''}), 200
    return jsonify({'result': False, 'error': "Invalid request"}), 400

@friendsRoutes.route('/info/<id>', methods=['POST'])
def getFriendInfo():
    return