# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing users

from app import app, db
from app.models import *
from flask_json import as_json


@app.route('/api/1/users/', methods=['GET'])
@as_json
def user_list():
    return {"message": "GET: List all users"}


@app.route('/api/1/users/', methods=['POST'])
@as_json
def user_add():
    return {"message": "POST: Add an user"}


@app.route('/api/1/users/<user_id>/', methods=['GET'])
@as_json
def user_show(user_id):
    return {"message": "GET: Show %s" % user_id}


@app.route('/api/1/users/<user_id>/', methods=['POST'])
@as_json
def user_update(user_id):
    return {"message": "POST: Update %s" % user_id}


@app.route('/api/1/users/<user_id>/', methods=['DELETE'])
@as_json
def user_delete(user_id):
    return {"message": "DELETE: Delete %s" % user_id}