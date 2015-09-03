# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Default configuration, used in development environment

import os
basepath = os.path.abspath(os.path.dirname(__file__))

# Environment
DEBUG   = True
TESTING = False

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basepath, "var", "database.db")
SHELVE_PATH = os.path.join(basepath, "var", "shelve.db")


# Json
JSON_AS_ASCII = False
JSON_SORT_KEYS = True
JSONIFY_PRETTYPRINT_REGULAR = True
JSON_DATETIME_FORMAT = "%Y-%m-%d %X"
JSON_DATE_FORMAT     = "%Y-%m-%d"
JSON_TIME_FORMAT     = "%X"

# Required to ensure HTTP exception handers work in debug & test
# See: http://flask.pocoo.org/docs/0.10/api/#flask.Flask.trap_http_exception
TRAP_HTTP_EXCEPTIONS = True