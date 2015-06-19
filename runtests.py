# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Run unit tests for this application

import os, sys, unittest

basepath = os.path.abspath(os.path.dirname(__file__))

# Add application root to PYTHON_PATH
sys.path.append(basepath + '/app')

# Set config environment before importing app
os.environ['FLASK_APP_CONFIG'] = basepath + "/config_testing.py"

from app import app, db
from app.routes import *
from app.models import *

if __name__ == "__main__":

    # Prepare app for testing
    db.create_all()

    suite = unittest.TestLoader().discover(basepath + '/test')
    unittest.TextTestRunner(verbosity=2).run(suite)