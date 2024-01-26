from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_restful import abort

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_rules = ('-events.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(450), nullable=False)
    
    events = db.relationship('Event', secondary='booked_events', back_populates='users')
    
        
    
    @validates('username')
    def checks_uniqueness(self, key, username):
        if User.query.filter_by(username=username).first():
            abort(400, 
                message=f"A user with the name '{username}' already exists. Please choose a different name."
            )
        else:
            return username
#   For Logout JWT Block List
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti =  db.Column(db.String(100),nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


class Organizer(db.Model, SerializerMixin):
    __tablename__ = 'organizers'
    serialize_rules = ('-events.organizer',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(450), nullable=False)
   
    
    events = db.relationship('Event', backref='organizer', lazy=True)
    
    @validates('username')
    def checks_uniqueness(self, key, username):
        if Organizer.query.filter_by(username=username).first():
            abort(400, 
                message=f"A user with the name '{username}' already exists. Please choose a different name."
            )
        else:
            return username

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    serialize_rules = ('-users.events', '-organizer.events', '-category.events',)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizers.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    users = db.relationship('User', secondary='booked_events', back_populates='events')

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    serialize_rules = ('-events.category',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    events = db.relationship('Event', backref='category', lazy=True)
    
class BookedEvent(db.Model, SerializerMixin):
    __tablename__ = 'booked_events'
    
    serialize_rules = ('-user.booked_events', '-event.booked_events',)
    
    id = db.Column(db.Integer, primary_key= True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))