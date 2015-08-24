# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing visitors

from app import app, db
from app.models import *
from flask_json import as_json


@app.route('/api/1/visitors/', methods=['GET'])
@as_json
def visitor_list():
    return {"message": "GET: List all visitors"}


@app.route('/api/1/visitors/', methods=['POST'])
@as_json
def visitor_add():
    return {"message": "POST: Add an visitor"}


@app.route('/api/1/visitors/<visitor_id>/', methods=['GET'])
@as_json
def visitor_show(visitor_id):
    return {"message": "GET: Show %s" % visitor_id}


@app.route('/api/1/visitors/<visitor_id>/', methods=['POST'])
@as_json
def visitor_update(visitor_id):
    return {"message": "POST: Update %s" % visitor_id}


@app.route('/api/1/visitors/<visitor_id>/', methods=['DELETE'])
@as_json
def visitor_delete(visitor_id):
    return {"message": "DELETE: Delete %s" % visitor_id}