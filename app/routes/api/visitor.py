# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing visitors

from app import app, db
from app.models import *


@app.route('/api/1/visitors/', methods=['GET'])
def visitor_list():
    return "GET: List all visitors"


@app.route('/api/1/visitors/', methods=['POST'])
def visitor_add():
    return "POST: Add an visitor"


@app.route('/api/1/visitors/<visitor_id>/', methods=['GET'])
def visitor_show(visitor_id):
    return "GET: Show %s" % visitor_id


@app.route('/api/1/visitors/<visitor_id>/', methods=['POST'])
def visitor_update(visitor_id):
    return "POST: Update %s" % visitor_id


@app.route('/api/1/visitors/<visitor_id>/', methods=['DELETE'])
def visitor_delete(visitor_id):
    return "DELETE: Delete %s" % visitor_id