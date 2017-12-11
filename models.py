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
#

class Testrequestday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    choice = db.Column(db.String(5))
    startTime = db.Column(db.Integer)
    endTime = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, choice, startTime, endTime, day, month, year, userID):
        self.day = day
        self.month = month
        self.year = year
        self.choice = choice
        self.startTime = startTime
        self.endTime = endTime
        self.user_id = userID

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True)
    pwHash = db.Column(db.String(120))
    employeeName = db.Column(db.String(50))
    testRequestDays = db.relationship('Testrequestday', backref='userID')
    
    def __init__(self, username, password, employeeName):
        newID = (User.query.order_by(User.id.desc()).first())
        if newID == None:
            newID = 0
        else:
            newID = newID.id + 1
        self.username = username
        self.pwHash = makePwHash(password)
        self.admin = 0
        self.employeeName = employeeName

# class Request(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     employeeID = db.Column(db.Integer)
#     month = db.Column(db.Integer)
#     year = db.Column(db.Integer)
#     request = db.Column(db.String(500)) #String in the form of a list of days D{No/Can/Yes}, 9, 9DNo/Can/Yes
#     rows = db.relationship('Requestrow', backref='request')


# class Requestrow(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     requestID = db.Column(db.Integer, db.ForeignKey('request.id'))
#     days = db.relationship('Requestday', backref='requestRow')
#     month = db.Column(db.Integer)
#     year = db.Column(db.Integer)

#     def __init__(self, request):
#         self.request = request
#         self.month = request.month
#         self.year = request.year





# class Requestday(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     requestRowID = db.Column(db.Integer, db.ForeignKey('requestrow.id'))
#     year = db.Column(db.Integer)
#     month = db.Column(db.Integer)
#     day = db.Column(db.Integer)
#     choice = db.Column(db.Integer)
#     startTime = db.Column(db.Integer)
#     endTime = db.Column(db.Integer)

#     def __init__(self, requestRow, day, choice, startTime, endTime):
#         self.requestRow = requestRow
#         self.year = requestRow.year
#         self.month = requestRow.month
#         self.day = day
#         self.choice = choice    
#         self.startTime = startTime
#         self.endTime = endTime
        
# class Schedule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     month = db.Column(db.Integer)
#     year = db.Column(db.Integer)
#     shifts = db.Column(db.String(1500)) #Each row will have 7 days, each day will have a number, 6-15 shifts
#     scheduleRows = db.relationship('Schedulerow', backref='schedule')

# class Schedulerow(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     scheduleID = db.Column(db.Integer, db.ForeignKey('schedule.id'))
#     days = db.relationship('Scheduleday', backref='scheduleRow')

#     def __init__(self, schedule):
#         self.schedule = schedule
    

# class Scheduleday(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     scheduleRowID = db.Column(db.Integer, db.ForeignKey('scheduleRow.id'))
#     shifts = db.relationship('Shift', backref='scheduleDay')
    
#     def __init__(self, scheduleRow):
#         self.scheduleRow = scheduleRow


# class Shift(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     scheduleDayID = db.Column(db.Integer, db.ForeignKey('scheduleDay.id'))
#     employeeID = db.Column(db.Integer)
#     role = db.Column(db.Integer) #0 for M, 1 for MA, 2 for A, 3 for C, 4 for R

#     def __init__(self, scheduleDay):
#         self.scheduleDay = scheduleDay #Object variable passed in