# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# URL routes for apps

from app import app, db
from models import User
from flask import render_template

@app.route('/')
def home():
    users = User.query.all()
    return render_template('layout.html', users=users)