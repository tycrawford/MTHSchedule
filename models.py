from app import db
import random

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True)
#     pwHash = db.Column(db.String(120))
#     #games = db.relationship('Games', backref='' #maybe connect with character, which has a game id column instead of games
#     gamesPlayed = db.Column(db.Integer, default=0)
#     score = db.Column(db.Integer, default=1000)

#     def __init__(self, username, password):
#         self.username = username
#         self.pwHash = makePwHash(password)

class Employee(db.model):
    id = db.Column(db.Integer, primary_key=True)
    employeeName = db.Column(db.String(50))

class Request(db.model):
    id = db.Column(db.Integer, primary_key=True)
    employeeID = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    request = db.Column(db.String(500)) #String in the form of a list of days DNo/Can/Yes, 9, 9DNo/Can/Yes
