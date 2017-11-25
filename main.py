from flask import Flask
from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import Employee
import datetime
from calendar import monthrange
#from hashutils import checkPwHash

@app.route("/month")
def month():
    month = request.args.get('month')
    year = request.args.get('year')
    startDay = datetime.date(year, month, 1).isoweekday() - 1
    lastDay = monthrange(year, month)[1]
    listDays = list(range(1, lastDay + 1))
    
    