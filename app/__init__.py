# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Flask apps and global objects

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


# The flask app
app = Flask(__name__)
app.config.from_object('config_default')


# Override default config with file specified in environment variable
if os.environ.get('FLASK_APP_CONFIG'):
    app.config.from_envvar('FLASK_APP_CONFIG')


# In dev or test, serve static files from site root
# In production this should be handled by the http service
if app.config.get('DEBUG') or app.config.get('TESTING'):
    from werkzeug import SharedDataMiddleware
    basepath = os.path.abspath(os.path.dirname(__file__))
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/': os.path.join(basepath, 'static')})


# The SQL DB object
db = SQLAlchemy(app)


## Helpful methods ##

def db_seed():
    """Rebuild the database populating it with seed data"""
    db.drop_all()
    db.create_all()
    db.session.add(User(name="Craig"))
    db.session.add(User(name="Vicky"))
    db.session.add(User(name="Sophie"))
    db.session.commit()


def db_show():
    """Display data in the DB"""
    for user in User.query.all(): print user