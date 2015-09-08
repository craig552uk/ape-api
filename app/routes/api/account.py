# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing accounts

from app import app, db
from app.models import *
from flask import request
from flask_json import as_json
from werkzeug.exceptions import NotFound, BadRequest


@app.route('/api/1/accounts/', methods=['GET'])
@as_json
def account_list():
    accounts = Account.query.all()
    return {'data': [a.to_dict() for a in accounts] }


@app.route('/api/1/accounts/', methods=['POST'])
@as_json
def account_add():
    data = request.args.get('data', dict())

    # TODO
    
    return {"data": "POST: Add an account"}


@app.route('/api/1/accounts/<account_id>/', methods=['GET'])
@as_json
def account_show(account_id):
    account = Account.query.filter_by(id=account_id).first()
    if not account: raise NotFound("No account exists with the id '%s'" % account_id)
    return {"data": account.to_dict()}


@app.route('/api/1/accounts/<account_id>/', methods=['POST'])
@as_json
def account_update(account_id):
    account = Account.query.filter_by(id=account_id).first()
    if not account: raise NotFound("No account exists with the id '%s'" % account_id)

    # TODO
    
    return {"data": "POST: Update %s" % account_id}


@app.route('/api/1/accounts/<account_id>/', methods=['DELETE'])
@as_json
def account_delete(account_id):
    account = Account.query.filter_by(id=account_id).first()
    if not account: raise NotFound("No account exists with the id '%s'" % account_id)
    
    # TODO
    
    return {"data": "DELETE: Delete %s" % account_id}