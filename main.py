from flask import Flask
from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User, Testrequestday, Shift
import datetime
from calendar import monthrange
from monthBuilding import makeCalendarHTML, makeCalendarList
from hashutils import checkPwHash
from makeChoiceList import makeChoiceList
from makeShiftFromTemplate import makeWeekTemplateFromScratchPhaseOne, modifyWeekOfShifts, makeWholeMonthShifts


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
    options = """<option value="viewrequest">Submit Request Off</option>
    <option value="viewschedule">View Schedule</option>
    """
    userInfo = User.query.filter_by(username=username).first()
    priv = userInfo.admin
    if priv == 1:
        options = options + """
        <option value="makefreshmonth">Make a Schedule from a Template</option>
        <option value="editschedule">Edit a Schedule</option>
        <option value="viewshifts">View My Shifts</option>
        """
    selectList = """<form action='/homepagererouter' method='post'>
    <label> Pick your option </label>
    <select name="option">{0}</select><br>
    <label> Month </label>
    <input name='month' type='number' min='1' max='12'>
    <label> Year </label>
    <input name='year' type='number' min='2017' max='2025'>
    <br>
    <input type='submit' value='GO!'>
    </form>
    """.format(options)

    return render_template('homepage.html', options=selectList)

@app.route("/homepagererouter", methods=['POST'])
def homepagererouter():
    year = request.form['year']
    month = request.form['month']
    option = request.form['option']
    if option == "viewrequest":
        return redirect("/month?year={0}&month={1}".format(year,month))
    elif option == "viewschedule":
        return redirect("/viewmonth?year={0}&month={1}".format(year,month))
    elif option == "editschedule":
        return redirect("/editmonth?year={0}&month={1}".format(year,month))
    elif option == "makefreshmonth":
        return redirect("/weekOfShifts")
    elif option == "viewshifts":
        return redirect("/shifts?year={0}&month={1}".format(year,month))

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
    times = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']

    username = session['username']
    year = request.args.get('year')
    month = request.args.get('month')
    userInfo = User.query.filter_by(username=username).first()
    shifts = Shift.query.filter_by(year=year, month=month,userId=userInfo.id).all()
    table = """
    <table border='1px'> <tr> <th>Day</th><th>Time In</th><th>Time Out</th></tr>

    """
    for shift in shifts:
        table = table + """
        <tr> <td> {1}/{2}/{0} </td> <td> {3} </td> <td> {4} </td> </tr>
        """.format(year, month,shift.day,times[shift.timeIn-8], times[shift.timeOut-8])
    table = table + "</table>"
    return render_template("month.html", table=table)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usernameError = ''
        passwordError = ''
        existingUser = User.query.filter_by(username=username).first()
        if not existingUser:
            userError = "Username not in the system"
            return render_template("login.html", usernameError=usernameError, passwordError=passwordError)
        else:
            if checkPwHash(password, existingUser.pwHash) == False:
                print("PASSWORD FAILED #####################################")

                passwordError = "Password not valid!"
                return render_template("login.html", usernameError=usernameError, passwordError=passwordError)
            else:
                session['username'] = username
                return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

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
            listOfShifts.append(int(request.form[str(i)]))
        table = modifyWeekOfShifts(listOfShifts)
        return render_template("month.html", table=table)

    if request.method == 'GET':
        table = makeWeekTemplateFromScratchPhaseOne()
        return render_template("month.html", table=table)

@app.route('/makewholemonth', methods=['POST'])
def makewholemonth():
    listOfShifts = []
    for i in range(7):
        listOfShifts.append(int(request.form[str(i)]))
    template = []
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for i in range(len(listOfShifts)):
        thisDaysShifts = []
        for j in range(listOfShifts[i]):
            thisShift = []
            thisShiftRole = request.form[str(days[i]+"role"+str(j))]
            thisShiftStart = request.form[str(days[i]+"start"+str(j))]
            thisShiftEnd = request.form[str(days[i]+"end"+str(j))]
            thisShift.append(thisShiftRole)
            thisShift.append(thisShiftStart)
            thisShift.append(thisShiftEnd)      #Add the List of Role, Start, and End to a small list
            thisDaysShifts.append(thisShift)    #Add that small list to a list of all shifts for the day
        template.append(thisDaysShifts)         #Add the day's worth of shifts to the template
    year = request.form['year']
    month = request.form['month']
    listOfDays = makeCalendarList(int(year), int(month))
    roles = ['M', 'MA', 'A', 'C', 'R']
    for rowOfDays in listOfDays:
        for i in range(len(rowOfDays)): #i represents the numerical equivalent of the day
            if rowOfDays[i] == "":
                continue
            else:
                for j in range(listOfShifts[i]): #j represents each shift of each day, listOfShifts has each days number of shifts indexed
                    todayRole = roles.index(template[i][j][0])
                    todayStart = template[i][j][1]
                    todayEnd = template[i][j][2]
                    day = rowOfDays[i]
                    newShift = Shift(day,month,year,todayRole,todayStart,todayEnd)
                    db.session.add(newShift)
                    db.session.commit()

    table = makeWholeMonthShifts(template, int(year), int(month))
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

@app.route("/viewmonth")
def viewmonth():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    shifts = Shift.query.filter_by(year=year, month=month).order_by(Shift.day.asc(),Shift.timeIn.asc()).all()
    startTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
    endTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']
    roles = ['M', 'MA', 'A', 'C', 'R']
    listForm = makeCalendarList(year, month)
    monthName = datetime.date(1900, month, 1).strftime('%B')
    htmlTable = """
    <h1 align="center">{0} {1} </h1>
    <br>
    <table width='100%' border='1px'> 
    <tr> 
    <th> Sunday </th> 
    <th> Monday </th> 
    <th> Tuesday </th> 
    <th> Wednesday </th> 
    <th> Thursday </th> 
    <th> Friday </th> 
    <th> Saturday </th> 
    </tr>""".format(monthName,str(year), str(month))
    for row in listForm:
        htmlTable += "<tr>"
        for i in range(len(row)):
            day = row[i]
            if day == "":
                htmlTable += "<td></td>"
            else:
                tableRows = ""
                for shift in shifts:
                    employee = User.query.filter_by(id=shift.userId).first()
                    if employee == None:
                        employeeName = "None"
                    else:
                        employeeName = employee.employeeName
                    if shift.day == day:
                        tableRows = tableRows + "<tr><td>" + roles[shift.role] + "</td><td>" + str(employeeName) + "</td><td>" + startTimes[shift.timeIn - 8] + "</td><td>" + endTimes[shift.timeOut - 8] + "</td></tr>"
                    
                htmlTable += """<td valign='top'>
                <day style='float: right'>{0}</day>
                <table border='1px' border-collapse='collapse'>
                <tr>
                <th>Role</th>
                <th>Employee</th>
                <th>Beg</th>
                <th>End</th>
                </tr>{1}</table></td>

                """.format(day,tableRows)
        htmlTable += "</tr>"
    htmlTable += "</table>"
    
    return htmlTable
    
@app.route("/editmonth")
def editmonth():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    shifts = Shift.query.filter_by(year=year, month=month).order_by(Shift.day.asc(),Shift.timeIn.asc()).all()
    startTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
    endTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']
    roles = ['M', 'MA', 'A', 'C', 'R']
    listForm = makeCalendarList(year, month)
    monthName = datetime.date(1900, month, 1).strftime('%B')
    htmlTable = """<form action='/assignshifts' method='post'>
    <input type='hidden' name='month' value='{2}'>
    <input type='hidden' name='year' value='{1}'>:
    <h1 align="center">{0} {1} </h1>
    <br>
    <table width='100%' border='1px'> 
    <tr> 
    <th> Sunday </th> 
    <th> Monday </th> 
    <th> Tuesday </th> 
    <th> Wednesday </th> 
    <th> Thursday </th> 
    <th> Friday </th> 
    <th> Saturday </th> 
    </tr>""".format(monthName,str(year), str(month))
    for row in listForm:
        htmlTable += "<tr>"
        for i in range(len(row)):
            day = row[i]
            if day == "":
                htmlTable += "<td></td>"
            else:
                tableRows = ""
                for shift in shifts:
                    employee = User.query.filter_by(id=shift.userId).first()
                    if employee == None:
                        employeeName = "None"
                    else:
                        employeeName = employee.employeeName
                    listOfEmployees = []
                    optionList = ""
                    if roles[shift.role] == "M":
                        employees = User.query.filter_by(role=0).all()
                    elif roles[shift.role] == "MA":
                        employees = User.query.filter_by(role='0').all()
                        extraEmployees = User.query.filter_by(role='2').all()

                    elif roles[shift.role] == "A":
                        employees = User.query.filter_by(role=2).all()
                    elif roles[shift.role] == "C":
                        employees = User.query.filter_by(role=3).all()
                    else:
                        employees = User.query.filter_by(role=4).all()
                    for employee in employees:
                        listOfEmployees.append(employee.employeeName)
                        optionList = optionList + "<option value='{0}'>{1}</option>".format(employee.id,employee.employeeName)
                    if roles[shift.role] == "MA":
                        for employee in extraEmployees:
                            listOfEmployees.append(employee.employeeName)
                            optionList = optionList + "<option value='{0}'>{1}</option>".format(employee.id,employee.employeeName)
                    if shift.day == day:
                        if employeeName == "None":
                            valueFiller = ""
                        else:
                            valueFiller = "value='{0}'".format(employeeName)
                        tableRows = tableRows + "<tr><td>" + roles[shift.role] + "</td><td>" + "<select name='{1}'{2}>{0}</select>".format(optionList,shift.id, valueFiller) + "</td><td>" + startTimes[shift.timeIn - 8] + "</td><td>" + endTimes[shift.timeOut - 8] + "</td></tr>"
                    
                htmlTable += """<td valign='top'>
                <day style='float: right'>{0}</day>
                <table border='1px' border-collapse='collapse'>
                <tr>
                <th>Role</th>
                <th>Employee</th>
                <th>Beg</th>
                <th>End</th>
                </tr>{1}</table></td>

                """.format(day,tableRows)
        htmlTable += "</tr>"
    htmlTable += "</table><label> Assign Shifts as Seen </label><input type='submit'>"
    
    return htmlTable

@app.route("/deleteshifts", methods=['GET', 'POST'])
def deleteshifts():
    if request.method == 'GET':
        year = int(request.args.get('year'))
        month = int(request.args.get('month'))
        shifts = Shift.query.filter_by(year=year, month=month).order_by(Shift.day.asc(),Shift.timeIn.asc()).all()
        startTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
        endTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']
        roles = ['M', 'MA', 'A', 'C', 'R']
        listForm = makeCalendarList(year, month)
        monthName = datetime.date(1900, month, 1).strftime('%B')
        htmlTable = """<form action='/delete' method='post'>
        <input type='hidden' name='month' value='{2}'>
        <input type='hidden' name='year' value='{1}'>:
        <h1 align="center">{0} {1} </h1>
        <br>
        Delete Shifts
        <br>
        <table width='100%' border='1px'> 
        <tr> 
        <th> Sunday </th> 
        <th> Monday </th> 
        <th> Tuesday </th> 
        <th> Wednesday </th> 
        <th> Thursday </th> 
        <th> Friday </th> 
        <th> Saturday </th> 
        </tr>""".format(monthName,str(year), str(month))
        for row in listForm:
            htmlTable += "<tr>"
            for i in range(len(row)):
                day = row[i]
                if day == "":
                    htmlTable += "<td></td>"
                else:
                    tableRows = ""
                    for shift in shifts:
                        employee = User.query.filter_by(id=shift.userId).first()
                        if employee == None:
                            employeeName = "None"
                        else:
                            employeeName = employee.employeeName
                        
                        if shift.day == day:
                            if employeeName == "None":
                                valueFiller = ""
                            else:
                                valueFiller = "value='{0}'".format(employeeName)
                            tableRows = tableRows + "<tr><td>" + roles[shift.role] + "</td><td>" + employeeName + "</td><td>" + startTimes[shift.timeIn - 8] + "</td><td>" + endTimes[shift.timeOut - 8] + "</td><td><input type='checkbox' name='{0}' value='delete'></td></tr>".format(shift.id)
                        
                    htmlTable += """<td valign='top'>
                    <day style='float: right'>{0}</day>
                    <table border='1px' border-collapse='collapse'>
                    <tr>
                    <th>Role</th>
                    <th>Employee</th>
                    <th>Beg</th>
                    <th>End</th>
                    <th>Del</th>
                    </tr>{1}</table></td>

                    """.format(day,tableRows)
            htmlTable += "</tr>"
        htmlTable += "</table><label> Delete Shifts as Seen </label><input type='submit'>"
        
        return htmlTable
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        shifts = Shift.query.filter_by(year=year,month=month).all()
        for shift in shifts:
            if request.form[str(shift.id)] == True:
                db.session.delete(shift)
                db.session.commit()


@app.route('/delete', methods=['POST'])
def delete():
    year = request.form['year']
    month = request.form['month']
    shifts = Shift.query.filter_by(year=year,month=month).all()

    for shift in shifts:
        print("GOT TO DELETE FOR LOOP")
        print(shift.id)
        if request.form.get(str(shift.id)) == "delete":
            print("GOT TO DELETE IF STATEMENT")
            Shift.query.filter_by(id=shift.id).delete()
            db.session.commit()  
          
        #return redirect("/deleteshifts?year={0}&month={1}".format(year,month))

@app.route("/assignshifts", methods=['POST'])
def assignshifts():
    year = request.form['year']
    month = request.form['month']
    shifts = Shift.query.filter_by(year=year, month=month).all()
    for shift in shifts:
        assignedEmployee = request.form[str(shift.id)]
        shift.assignShift(assignedEmployee)
        db.session.commit()
    return redirect("/viewmonth?year={0}&month={1}".format(year,month))
if __name__ == "__main__":
    app.run()