# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing accounts

from app import app, db
from app.models import *
from flask_json import as_json


@app.route('/api/1/accounts/', methods=['GET'])
@as_json
def account_list():
    return {"mesage": "GET: List all accounts"}


@app.route('/api/1/accounts/', methods=['POST'])
@as_json
def account_add():
    return {"message": "POST: Add an account"}


@app.route('/api/1/accounts/<account_id>/', methods=['GET'])
@as_json
def account_show(account_id):
    return {"message": "GET: Show %s" % account_id}


@app.route('/api/1/accounts/<account_id>/', methods=['POST'])
@as_json
def account_update(account_id):
    return {"message": "POST: Update %s" % account_id}


@app.route('/api/1/accounts/<account_id>/', methods=['DELETE'])
@as_json
def account_delete(account_id):
    return {"message": "DELETE: Delete %s" % account_id}