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
    data    = request.get_json() or dict()
    name    = data.get('name', str())
    sites   = data.get('sites', list())
    enabled = data.get('enabled', True)
    if not name: raise BadRequest("Name required")

    account = Account(name=name, sites=sites, enabled=enabled)
    
    if 'user_ids' in data.keys():
        account.users = User.query.filter(User.id.in_(data['user_ids'])).all()    

    db.session.add(account)
    db.session.commit()
    db.session.refresh(account)
    return {"data": account.to_dict()}


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

    data = request.get_json() or dict()
    if 'name'    in data.keys(): account.name    = data['name']
    if 'sites'   in data.keys(): account.sites   = data['sites']
    if 'enabled' in data.keys(): account.enabled = data['enabled']

    if 'user_ids' in data.keys():
        account.users = User.query.filter(User.id.in_(data['user_ids'])).all()

    db.session.add(account)
    db.session.commit()
    db.session.refresh(account)
    return {"data": account.to_dict()}


@app.route('/api/1/accounts/<account_id>/', methods=['DELETE'])
@as_json
def account_delete(account_id):
    account = Account.query.filter_by(id=account_id).first()
    if not account: raise NotFound("No account exists with the id '%s'" % account_id)
    
    db.session.delete(account)
    db.session.commit()
    return {"data": "Account (%s) deleted" % account_id}