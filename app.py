from flask import Flask,render_template,url_for,redirect,request,session
from models import *
import time
from sqlalchemy import func
from functools import wraps
import Config
import getTime
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

