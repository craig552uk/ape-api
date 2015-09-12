# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Flask apps and global objects

import os
import sys

# Add (non-pip) 3rd party libraries to sys path
basepath = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(basepath, "lib"))

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON

# The flask app
app = Flask(__name__)
app.config.from_object('config_default')

# Enable JSON responses
json_app = FlaskJSON(app)

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