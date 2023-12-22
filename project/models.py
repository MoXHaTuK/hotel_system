from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(0))

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    alcohol = db.Column(db.String(100))
    spice = db.Column(db.String(100))
    color = db.Column(db.String(100))
    music = db.Column(db.String(100))

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer)
    color = db.Column(db.String(100))
    beds = db.Column(db.Integer)
    price = db.Column(db.Integer)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    payment = db.Column(db.Integer)