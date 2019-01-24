from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from setting import app

db= SQLAlchemy(app)

class User(db.Model):
    __tablename__= 'users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(80), unique=True, nullable=False)
    username=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(256),nullable=False )

    def __repr__(self):
        return str({
            'name':self.name,
            'email':self.email,
            'username':self.username,
            'password':self.password
            })
    
    def username_password_match(_username,_password):
        user= User.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True

    def getAllUsers():
        return User.query.all()

    def createUser(_name,_email,_username,_password):
        new_user= User(name=_name,email=_email,username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()
    

