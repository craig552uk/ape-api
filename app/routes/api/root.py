# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API root endpoints, auth handlers and error handlers

from app import app
from werkzeug.exceptions import Unauthorized

@app.route('/api/')
def api_root(): raise Unauthorized
    
@app.route('/api/1/')
def api_root_1(): raise Unauthorized
