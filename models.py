from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True)   
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

class Vessel(db.Model):
    __tablename__ = "vessels"
    id = db.Column(db.Integer, primary_key=True)
    vessel_name = db.Column(db.String(200), nullable=False)
    imo_number = db.Column(db.String(20), unique=True)
    vessel_type = db.Column(db.String(100))
    flag = db.Column(db.String(50))
    build_year = db.Column(db.Integer)
 
