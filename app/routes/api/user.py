# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing users

from app import app, db
from app.models import *


@app.route('/api/1/users/', methods=['GET'])
def user_list():
    return "GET: List all users"


@app.route('/api/1/users/', methods=['POST'])
def user_add():
    return "POST: Add an user"


@app.route('/api/1/users/<user_id>/', methods=['GET'])
def user_show(user_id):
    return "GET: Show %s" % user_id


@app.route('/api/1/users/<user_id>/', methods=['POST'])
def user_update(user_id):
    return "POST: Update %s" % user_id


@app.route('/api/1/users/<user_id>/', methods=['DELETE'])
def user_delete(user_id):
    return "DELETE: Delete %s" % user_id