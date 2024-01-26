from models import db, User, TokenBlocklist
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, Api
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth_bp', __name__)
api = Api(auth_bp)


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                return jsonify(access_token=access_token)

            return {"error": "Wrong Password!"}, 401

        else:
            return {"error": "User doesn't exist!"}, 404


class AuthenticatedUserResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()  # Getting current user id
        user = User.query.get(current_user_id)


        if user:
            event_dict =[{
            "id":event.id,
            "title": event.title,
            "description": event.description,
            "image_url":event.image_url,
            "start_time": event.start_time,
            "end_time": event.end_time
            
        } for event in user.events]
            user_data = {
                'id': user.id,
                'username': user.username,
                'phone': user.phone,
                'email': user.email,
                'events': event_dict
            }
            return user_data, 200
        else:
            return {"error": "User not found"}, 404


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jwt_token = get_jwt()
        jti = jwt_token['jti']

        token_blocklist = TokenBlocklist(jti=jti)
        db.session.add(token_blocklist)
        db.session.commit()

        return {"success": "Logged out successfully!"}, 200


# Add resources to the API
api.add_resource(LoginResource, '/login')
api.add_resource(AuthenticatedUserResource, '/authenticated_user')
api.add_resource(LogoutResource, '/logout')
