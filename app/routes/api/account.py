# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing accounts

from app import app, db
from app.models import *


@app.route('/api/1/accounts/', methods=['GET'])
def account_list():
    return "GET: List all accounts"


@app.route('/api/1/accounts/', methods=['POST'])
def account_add():
    return "POST: Add an account"


@app.route('/api/1/accounts/<account_id>/', methods=['GET'])
def account_show(account_id):
    return "GET: Show %s" % account_id


@app.route('/api/1/accounts/<account_id>/', methods=['POST'])
def account_update(account_id):
    return "POST: Update %s" % account_id


@app.route('/api/1/accounts/<account_id>/', methods=['DELETE'])
def account_delete(account_id):
    return "DELETE: Delete %s" % account_id