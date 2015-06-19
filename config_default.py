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

# Json
JSON_AS_ASCII = False
JSON_SORT_KEYS = True
JSONIFY_PRETTYPRINT_REGULAR = True