# from .app import app, db
import os #To handle files path
from flask import Flask, render_template, redirect, request, g, session #Main Flask
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user #To create the Login
from flask_sqlalchemy import SQLAlchemy #SQL Alchemy to create the database
import sys


files_path = os.path.dirname(os.path.abspath(__file__)) #Setting the path of the main directory
database_main_file = "sqlite:///{}".format(os.path.join(files_path, "primary.db")) #The path of the main database

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_main_file
app.secret_key = "A06748581"

login = LoginManager()
login.init_app(app)
login.login_view = 'login'

db = SQLAlchemy(app)
