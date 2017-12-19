from flask import Flask
from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User, Testrequestday
import datetime
from calendar import monthrange
from monthBuilding import makeCalendarHTML
from hashutils import checkPwHash
from makeChoiceList import makeChoiceList
from makeShiftFromTemplate import makeWeekTemplateFromScratchPhaseOne, modifyWeekOfShifts
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'month']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    username = session['username']
    #TODO add an options table here
    #TODO if admin = 1 then the user is an admin
    #TODO Give all users the options to view/edit their requests
    #TODO Give all users the options to view the schedule for whichever month
    #TODO Give admins the option to view/edit the shift template
    #TODO Give admins the option to generate the schedule
    #TODO Give admins the option to publish the schedule
    #TODO GIve admins the option to add a month for requests.
    options = "Your Request Off Form <br> View Schedule <br>"
    userInfo = User.query.filter_by(username=username).first()
    priv = userInfo.admin
    if priv == 1:
        options = options + "View/Edit Shifts <br> Generate a Schedule <br> Publish a Schedule <br> Add A Schedule <br>"

    return render_template('homepage.html', options=options)
@app.route('/myrequests')
def myRequests():
    username = session['username']
    userInfo = User.query.filter_by(username=username).first()
    #TODO Recall information about the user to generate a list of hyperlinks to pull a request month for the user.
    #The idea is to see what months are available for the user to look at. Specifically, those for previous months. 
    return render_template('base.html')

@app.route('/monthselect')
def monthselect():
    function = request.args.get('function')
    return render_template("monthselect.html")

@app.route('/shifts')
def shifts():
    username = session['username']
    userInfo = User.query.filter_by(username=username).first()
    if userInfo.admin == 0:
            return redirect("login")
    #TODO add a month select
    #
    table = ""

    return render_template("month.html", table=table)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Builds the path for a user signup page """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        employeeName = request.form['name']
        usernameError = ""
        passwordError = ""
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            usernameError = "Username already in use!"
        if len(username) < 3 or len(username) > 20:
            usernameError = "Username must be between 3 and 20 characters long"
        if len(password) < 3 or len(password) > 20:
            passwordError = "Password must be between 3 and 20 characters long"
        if password != confirm:
            passwordError = "Passwords do not match!"
        if passwordError == "" and usernameError == "":
            newUser = User(username, password, employeeName)
            db.session.add(newUser)
            db.session.commit()
            session['username'] = username
            return redirect("/")
        else:
            return render_template("usersignup.html", usernameError=usernameError, passwordError=passwordError)
    else:
        return render_template("usersignup.html")
#This section is where I intend to prototype small features as I make things more and more functional until I get to the scale I want to achieve

@app.route('/weekOfShifts', methods=['GET', 'POST'])
def weekOfShifts():
    if request.method == 'POST':
        listOfShifts = []
        for i in range(7):
            listOfShifts.append(request.form[i])
        table = modifyWeekOfShifts(listOfShifts)
        return render_template("month.html", table=table)
    if request.method == 'GET':
        table = makeWeekTemplateFromScratchPhaseOne()
        return render_template("month.html", table=table)

@app.route("/testrequestday", methods=['GET', 'POST'])
def testrequestday():

    startTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
    endTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']
    choices = ['Work', 'Available', 'OFF']
    if request.method == 'GET':
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')
        employeeID = request.args.get('employeeID')
        #Query the database for requestDays with the month, year, day, and employee, should only be one. 
        #TODO, make sure you find a way to only let one employee have a max of one request per day.
        thisRequest = Requestday.query.filter_by(month=month,day=day,year=year,employeeID=employeeID).first()
        prevChoice = ""
        prevStart = 0
        prevEnd = 0
        if type(thisRequest) != None:
            prevChoice = thisRequest.choice
            prevStart = str(thisRequest.startTime)
            prevEnd = str(thisRequest.endTime)
        selectStart = makeChoiceList(startTimes,startTime,prevStart)
        selectEnd = makeChoiceList(endTimes,endTime,prevEnd)
        selectChoice = makeChoiceList(choices,choice, prevChoice)
    
        
        return render_template("requestday.html", selectChoice=selectChoice, selectStart=selectStart, selectEnd=selectEnd, year=year, month=month, day=day)
    elif request.method == 'POST':
        #Take data in from a Post
        #Check to see if the employee in question has a request for the day given
        #If the employee does not have a request, make one with the passed data
        #If they do have a request, import the previous request, and set the requests choice and times to those from the form
        #Make sure to run through making a select start, end, an choice string, so that we can see what the user has just chosen
        newChoice = request.form['choice']
        newStart = request.form['start']
        newEnd = request.form['end']
        newMonth = request.form['month']
        newYear = request.form['year']
        newDay = request.form['day']
        newEmployee = request.form['employee']
        employeeID = Testemployee.query.filter_by(employeeName=newEmployee).first()
        employeeID = employeeID.id
        prevRequest = Testrequestday.query.filter_by(employeeID=employeeID, month=month, year=year, day=day).first()
        if type(prevRequest) == None:
            newRequest = testrequestday(newYear, newMonth, newDay, employeeID, newChoice, newStart, newEnd)
            db.session.add(newRequest)
            db.commit()
        else:
            prevRequest.choice = newChoice
            prevRequest.start = newStart
            prevRequest.end = newEnd
            db.commit()
        selectStart = makeChoiceList(startTimes, startTime, newChoice)
        selectEnd = makeChoiceList(endTimes, endTime, newEnd)
        selectChoice = makeChoiceList(choices, choice, newChoice)
        return render_template("requestday.html", selectChoice=selectChoice, selectStart=selectStart, selectEnd=selectEnd, year=year, month=month, day=day)


@app.route("/month", methods=['GET', 'POST'])
def month():
    if request.method == 'GET':
        month = int(request.args.get('month'))
        year = int(request.args.get('year'))
        htmlTable = makeCalendarHTML(year,month)
        return render_template("month.html", table=htmlTable)
    if request.method =='POST':
        allChoice = []
        allStart = []
        allEnd = []
        userID = User.query.filter_by(username=session['username']).first()
        userID = userID.id
        print(userID)
        numDays = monthrange(int(request.form['year']), int(request.form['month']))[1]
        for i in range(1,(numDays + 1)):
            allChoice.append(request.form['{0}choice'.format(i)])
            allStart.append(request.form['{0}startTime'.format(i)])
            allEnd.append(request.form['{0}endTime'.format(i)])
        outputHTML = ""
        for i in range(len(allChoice)):
            newRequest = Testrequestday(allChoice[i],allStart[i],allEnd[i],(i + 1), request.form['month'], request.form['year'], userID)
            db.session.add(newRequest)
            db.session.commit()


            #TODO Rather than build a list and then iterate through that list with another for loop, use this for loop to build request day objects
        for choice in range(len(allChoice)):
            outputHTML = outputHTML + "<br> {0}/{1}/{2} <br> Choice: ".format(request.form['month'], str(choice + 1), request.form['year']) + str(allChoice[choice]) + "<br> Start: " + str(allStart[choice]) + "<br> End: " +str(allEnd[choice]) + "<br>"

        return(outputHTML)

if __name__ == "__main__":
    app.run()