from models import db, Organizer, TokenBlocklist
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, Api
from werkzeug.security import check_password_hash

orgauth_bp = Blueprint('orgauth_bp', __name__)
api = Api(orgauth_bp)


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        organizer = Organizer.query.filter_by(username=username).first()

        if organizer:
            if check_password_hash(organizer.password, password):
                access_token = create_access_token(identity=organizer.id)
                return jsonify(access_token=access_token)

            return {"error": "Wrong Password!"}, 401

        else:
            return {"error": "Organizer doesn't exist!"}, 404


class AuthenticatedOrganizerResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()  # Getting current organizer id
        organizer = Organizer.query.get(current_user_id)


        if organizer:
            event_dict =[{
            "id":event.id,
            "title": event.title,
            "description": event.description,
            "image_url":event.image_url,
            "start_time": event.start_time,
            "end_time": event.end_time
            
        } for event in organizer.events]
            user_data = {
                'id': organizer.id,
                'username': organizer.username,
                'phone': organizer.phone,
                'email': organizer.email,
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
api.add_resource(LoginResource, '/login_organizer')
api.add_resource(AuthenticatedOrganizerResource, '/authenticated_organizer')
api.add_resource(LogoutResource, '/logout_organizer')
