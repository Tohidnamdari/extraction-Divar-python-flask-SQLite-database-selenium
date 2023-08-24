from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SECRET_KEY']='jhvhijghlkbvhjvjkjhvcj'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Text)
    password = db.Column(db.Text)
    def __repr__(self):
        return f'Users({self.username},{self.password})'
class home(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    metr = db.Column(db.Text)
    allmony = db.Column(db.Text)
    all_int = db.Column(db.Text)
    mony = db.Column(db.Text)
    mony_int = db.Column(db.Text)
    karbar = db.Column(db.Text)
    tabage = db.Column(db.Text)
    salsakht = db.Column(db.Text)
    room = db.Column(db.Text)
    def __repr__(self):
        return f'home({self.id},{self.name},{self.metr},{self.allmony},{self.mony},{self.karbar},{self.tabage},{self.salsakht},{self.room})'
