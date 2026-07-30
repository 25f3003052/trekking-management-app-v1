# Datbase define 
# SQLALchemy ->  ORM(Object Relation Model)

from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

db = SQLAlchemy()

# User model

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(180), unique=True, nullable=False)
    name =  db.Column(db.String(180), nullable=False)
    email_id = db.Column(db.String(180), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False) # special resion _pasword
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    pincode = db.Column(db.Integer)
    address = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean,default=False)
    is_blocked = db.Column(db.Boolean,default=False)

    
    def set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self._password,password) # T or F

    bookings = db.relationship(
        'Booking',
        backref='user',
        lazy=True,
        cascade = 'all , delete-orphan'
    )



class Staff(db.Model):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(180), unique=True, nullable=False)
    name =  db.Column(db.String(180), nullable=False)
    email_id = db.Column(db.String(180), unique=True, nullable=False)
    _password = db.Column("password", db.String(180), nullable=False) # special resion _pasword
    phone = db.Column(db.String(20))
    experience = db.Column(db.String(200))
    is_approved = db.Column(db.Boolean,default=False)
    is_blocked = db.Column(db.Boolean,default=False)

    def set_password(self,password):
        self._password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self._password,password) # T or F
    
    treks = db.relationship(
        "Trek",
        backref="assigned_staff",
        lazy=True
    )
