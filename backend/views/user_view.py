from models import db, User
from flask import request, jsonify, Blueprint, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api, abort
from werkzeug.security import generate_password_hash


user_bp = Blueprint('user_bp', __name__)
api = Api(user_bp)


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id is not None:
            user = User.query.get(user_id)
            if user:
                return jsonify({
                    'id': user.id,
                    'username': user.username,
                    'phone': user.phone,
                    'email': user.email
                }), 200
            else:
                return {"error": "User not found!"}, 404
        else:
            users = User.query.all()
            user_list = [{
                'id': user.id,
                'username': user.username,
                'phone': user.phone,
                'email': user.email
            } for user in users]
            return user_list, 200

    @jwt_required()
    def put(self):
        user = User.query.get(get_jwt_identity())
        data = request.get_json()

        if user:
            username = data['username']
            email = data['email']
            phone = data['phone']

            # Check if the new values already exist for other users/ NOTE THIS
            check_username = User.query.filter(User.id != get_jwt_identity(), User.username == username).first()
            check_email = User.query.filter(User.id != get_jwt_identity(), User.email == email).first()
            check_phone = User.query.filter(User.id != get_jwt_identity(), User.phone == phone).first()

            if check_username or check_email or check_phone:
                return jsonify({"error": "User email/username/phone already exist!"}), 400

            else:
                user.username = username
                user.email = email
                user.phone = phone

                db.session.commit()
                return {"success": "User updated successfully"}, 200

        else:
            return {"error": "User you are trying to update doesn't exist!"}, 404

    @jwt_required()
    def delete(self):
        user = User.query.get(get_jwt_identity())

        if user:
            db.session.delete(user)
            db.session.commit()
            return {"success": "User deleted successfully"}, 200

        else:
            return {"error": "User you are trying to delete is not found!"}, 404


class AddUserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        phone = data['phone']
        password = generate_password_hash(data['password'])

        check_username = User.query.filter_by(username=username).first()
        check_email = User.query.filter_by(email=email).first()
        check_phone = User.query.filter_by(phone=phone).first()

        if check_username or check_email or check_phone:
            return {"error": "User email/username/phone already exist!"}, 400

        else:
            new_user = User(email=email, password=password, username=username, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            return {"success": "User added successfully"}, 201


api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(AddUserResource, '/users')


