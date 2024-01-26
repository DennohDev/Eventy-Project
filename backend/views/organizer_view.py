from models import db, Organizer
from flask import request, jsonify, Blueprint, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api, abort
from werkzeug.security import generate_password_hash


organizer_bp = Blueprint('organizer_bp', __name__)
api = Api(organizer_bp)


class OrganizerResource(Resource):
    @jwt_required()
    def get(self, organizer_id=None):
        if organizer_id is not None:
            organizer = Organizer.query.get(organizer_id)
            if organizer:
                return jsonify({
                    'id': organizer.id,
                    'username': organizer.username,
                    'phone': organizer.phone,
                    'email': organizer.email
                }), 200
            else:
                return {"error": "Organizer not found!"}, 404
        else:
            organizers = Organizer.query.all()
            user_list = [{
                'id': organizer.id,
                'username': organizer.username,
                'phone': organizer.phone,
                'email': organizer.email
            } for organizer in organizers]
            return user_list, 200

    @jwt_required()
    def put(self):
        organizer = Organizer.query.get(get_jwt_identity())
        data = request.get_json()

        if organizer:
            username = data['username']
            email = data['email']
            phone = data['phone']

            # Check if the new values already exist for other users/ NOTE THIS
            check_username = Organizer.query.filter(Organizer.id != get_jwt_identity(), Organizer.username == username).first()
            check_email = Organizer.query.filter(Organizer.id != get_jwt_identity(), Organizer.email == email).first()
            check_phone = Organizer.query.filter(Organizer.id != get_jwt_identity(), Organizer.phone == phone).first()

            if check_username or check_email or check_phone:
                return jsonify({"error": "Organizer email/username/phone already exist!"}), 400

            else:
                organizer.username = username
                organizer.email = email
                organizer.phone = phone

                db.session.commit()
                return {"success": "Organizer updated successfully"}, 200

        else:
            return {"error": "Organizer you are trying to update doesn't exist!"}, 404

    @jwt_required()
    def delete(self):
        organizer = Organizer.query.get(get_jwt_identity())

        if organizer:
            db.session.delete(organizer)
            db.session.commit()
            return {"success": "Organizer deleted successfully"}, 200

        else:
            return {"error": "Organizer you are trying to delete is not found!"}, 404


class AddOrganizerResource(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        phone = data['phone']
        password = generate_password_hash(data['password'])

        check_username = Organizer.query.filter_by(username=username).first()
        check_email = Organizer.query.filter_by(email=email).first()
        check_phone = Organizer.query.filter_by(phone=phone).first()

        if check_username or check_email or check_phone:
            return {"error": "Organizer email/username/phone already exist!"}, 400

        else:
            new_user = Organizer(email=email, password=password, username=username, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            return {"success": "Organizer added successfully"}, 201


api.add_resource(OrganizerResource, '/organizers', '/organizer/<int:organizer_id>')
api.add_resource(AddOrganizerResource, '/organizers')


