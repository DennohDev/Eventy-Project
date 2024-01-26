from datetime import timedelta
from models import db, User, TokenBlocklist
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import abort

from models import  User, Event, Organizer, Category, BookedEvent, db

from views import *
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"


CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager()
app.config["JWT_SECRET_KEY"] = "2ab4c28f-a24d-4b78-a416-1b01d87cdb9c"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

# Operations CRUD
@app.route('/')
def hello():
    return "Welcome to the Eventy domain API"
# JWT LOADER
@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    if token:
        return token 
    else:
        return None



class UserByID(Resource):
     
    def get(self, id):
        with app.app_context():
            current_user = get_jwt_identity()
        
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return make_response(
                jsonify({"Message":"User not found"}),
                404
            )
        
        event_dict =[{
            "id":event.id,
            "title": event.title,
            "description": event.description,
            "image_url":event.image_url,
            "start_time": event.start_time,
            "end_time": event.end_time
            
        } for event in user.events]
        
        response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "events": event_dict
            
        }
        return response, 200
        
        
    
    def patch(self, id):
       
        
        user = User.query.filter_by(id=id).first()
        
        data = request.get_json()
        for attr, value in data.items():
            setattr(user, attr, value)
            
        db.session.add(user)
        db.session.commit()
        

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        
        if user:
            Event.query.filter_by(user_id=id).delete()
            
            try:
                db.session.delete(user)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 500
            
            response = make_response(jsonify({'message': 'User record successfully deleted'}), 204)
            return response


api.add_resource(UserByID, '/users/<int:id>')
        
    
class OrganizerRegistration(Resource):
    def post(self):
        data = request.get_json()
        
        organizer = Organizer(
            
            username=data['username'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
                 
        )
        
        try:
            db.session.add(organizer)
            db.session.commit()
            
        
        except Exception as e:
            db.session.rollback()
            abort(500, error=f"Error creating organizer: {str(e)}") 
        
        finally:
            db.session.close()
        
        response = make_response(jsonify({'Message': 'Organizer successfully created'}), 201)
        return response
    
    def get(self):
        organizers = Organizer.query.all()
        
        if not organizers:
            abort(404, message="No organizer records found")
        
        response = [{
            "id": organizer.id,
            "username": organizer.username,
            "email": organizer.email,
            "phone": organizer.phone,
            "password": organizer.password,
              } for organizer in organizers] 
        
        
        return make_response(
            jsonify(response),
            200
        )
    def login(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            abort(400, error="Both username and password are required for login")

        organizer = Organizer.query.filter_by(username=username, password=password).first()

        if not organizer:
            abort(401, error="Invalid username or password")

        response = make_response(jsonify({'Message': 'Login successful'}), 200)
        return response

api.add_resource(OrganizerRegistration, '/organizers')
api.add_resource(OrganizerRegistration, '/organizers/login', endpoint='login')  

        
    
class OrganizerByID(Resource):
    
    def get(self, id):
        organizer = Organizer.query.filter_by(id=id).first()
        
        if not organizer:
            return make_response(
                jsonify({"Message":"Organizer not found"}),
                404
            )
        
        event_dict =[{
            "id":event.id,
            "title": event.title,
            "description": event.description,
            "image_url":event.image_url,
            "start_time": event.start_time,
            "end_time": event.end_time
            
        } for event in organizer.events]
        
        response = {
            "id": organizer.id,
            "username": organizer.username,
            "email": organizer.email,
            "password": organizer.password,
            "events": event_dict
            
        }
        
        return make_response (
            jsonify(response),
            200
        )
    
    def patch(self, id):
         
        organizer = Organizer.query.filter_by(id=id).first()
        
        data = request.get_json()
        for attr, value in data.items():
            setattr(organizer, attr, value)
            
        db.session.add(organizer)
        db.session.commit()
        
        
    
    def delete(self, id):
        
        organizer = Organizer.query.filter_by(id=id).first()
        
        if organizer:
            Event.query.filter_by(organizer_id=id).delete()
            
            try:
                db.session.delete(organizer)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 500
            
            response = make_response(jsonify({'Message': 'Organizer record successfully deleted'}), 200)
            return response
            
        
        db.session.delete(organizer)
        db.session.commit()
        
        return make_response({'Message': 'User record successfully deleted'}, 200 )

api.add_resource(OrganizerByID, '/organizers/<int:id>')
        
    
class Events(Resource):
    def get(self): 
        events = Event.query.all()
    
        response= [{
                "id":event.id,
                "title": event.title,
                "description": event.description,
                "image_url":event.image_url,
                "start_time": event.start_time,
                "end_time": event.end_time
            } for event in events ]
            
        if not response:
            jsonify({"error":"Events not found"}, 404) 
        
        return make_response(
            jsonify(response),
            200
        )
            
 
    def post(self):
        
        data = request.get_json()
        
        event = Event (
            title = data['title'],
            description = data['description'],
            image_url = data['image_url'],
            start_time = data['start_time'],
            end_time = data['end_time'],
            organizer_id = data['organizer_id'],
            category_id = data['category_id'],
                       
        )
        
        try: 
            db.session.add(event)
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            abort(500, error=f"Error creating an event: {str(e)}")
        
        finally:
             db.session.close()
             
api.add_resource(Events, '/events')
            
            

class EventByID(Resource):
    def get(self, id):
        event = Event.query.filter_by(id=id).first()
        
        if not event:
            return make_response(
                jsonify({'message':'event record not found'}),
                404
            )
        
        response = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "image_url": event.image_url,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "organizer": event.organizer.username,
            "category": event.category.name
        }

        return make_response(
            jsonify(response),
            200
        )
            
    
    def patch(self, id):
        event = Event.query.filter_by(id=id).first()
        
        data = request.get_json()
        for attr, value in data.items():
            setattr(event , attr, value)
            
        db.session.add(event)
        db.session.commit()
        

    def delete(self, id):
        event = Event.query.filter_by(id=id).first()
        
        db.session.delete(event)
        db.session.commit()
        
        return make_response({'message': 'User record successfully deleted'}, 200 )

api.add_resource(EventByID, '/events/<int:id>')
 
class Categories(Resource):
    def get(self):
        
        categories = Category.query.all()
        
        response = [{
            'id': category.id,
            'name': category.name
        } for category in categories]
        
        return make_response(
            jsonify(response),
            200
        )

api.add_resource(Categories, '/categories')
        
        
class CategoryByID(Resource):
    def get(self, id):
        
        category = Category.query.filter_by(id=id).first()
        
        if not category:
            return make_response(
                jsonify({"error":"Category not Found"}),
                404
                )
        
        else:
            
            event_dict = [{
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "image_url":event.image_url,
                "start_time": event.start_time,
                "end_time": event.end_time
                
            } for event in category.events        
            ]
            
            response_data = {
                "id": category.id,
                "name": category.name,
                "events": event_dict
            }
            
            return make_response(
                jsonify(response_data),
                200
            )
            
api.add_resource(CategoryByID, '/categories/<int:id>')

class BookedEvents(Resource):
    def post(self):
        data = request.get_json()
        
        booked_event = BookedEvent (
            
            event_id = data['event_id'],
            user_id = data['user_id'],
            
        )
        
        try: 
            db.session.add(booked_event)
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            abort(500, error=f"Error booking an event: {str(e)}")
        
        finally:
             db.session.close()
        
api.add_resource(BookedEvents, '/bookedevents')

if __name__ == '__main__':
    app.run(port=5000, debug=True)