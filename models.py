from app import db
from hashutils import makePwHash
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Integer)
    employeeID = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True)
    pwHash = db.Column(db.String(120))
    
    def __init__(self, username, password, employeeName):

        newID = (User.query.order_by(User.id.desc()).first())
        if newID == None:
            newID = 0
        else:
            newID = newID.id
        newEmpID = (Employee.query.order_by(Employee.id.desc()).first())
        if newEmpID == None:
            newEmpID = 0
        else:
            newEmpID = newEmpID.id

        self.username = username
        self.pwHash = makePwHash(password)
        self.admin = 0
        newEmployee = Employee(employeeName, newID)
        db.session.add(newEmployee)
        db.session.commit()
        employeeID = Employee.query.filter_by(employeeID=newID).first()
        self.employeeID = employeeID.id

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employeeName = db.Column(db.String(50))
    employeeID = db.Column(db.Integer)

    def __init__(self, employeeName, employeeID):
        self.employeeName = employeeName
        self.employeeID = employeeID


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employeeID = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    request = db.Column(db.String(500)) #String in the form of a list of days D{No/Can/Yes}, 9, 9DNo/Can/Yes

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    shifts = db.Column(db.String(1500)) #Each row will have 7 days, each day will have a number, 6-15 shifts

