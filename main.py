from flask import Flask
from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import Employee
#from hashutils import checkPwHash