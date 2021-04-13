from flask_login import UserMixin
from . import db
from datetime import datetime



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    
    cars = db.relationship('Car', backref='user')
    

class Car(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_make = db.Column(db.String(100))
    car_model = db.Column(db.String(100))
    car_year = db.Column(db.String(100))
    color = db.Column(db.String(100))
    reg_plate = db.Column(db.String(100),unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    detection = db.relationship('Detection', backref ='car')
   
class Detection(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
   