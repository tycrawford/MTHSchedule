from flask import Flask
from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User, Employee, Request
import datetime
from calendar import monthrange
from hashutils import checkPwHash

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    username = session['username']

    return render_template('base.html')

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

@app.route("/month")
def month():
    month = request.args.get('month')
    year = request.args.get('year')
    startDay = datetime.date(year, month, 1).isoweekday() - 1
    lastDay = monthrange(year, month)[1]
    listDays = list(range(1, lastDay + 1))
    
    
if __name__ == "__main__":
    app.run()