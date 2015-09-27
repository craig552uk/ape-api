# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing users

from app import app, db
from app.models import *
from flask import request
from flask_json import as_json
from werkzeug.exceptions import NotFound, BadRequest

@app.route('/api/1/users/', methods=['GET'])
@as_json
def user_list():
    users = User.query.all()
    return {'data': [u.to_dict() for u in users]}


@app.route('/api/1/users/', methods=['POST'])
@as_json
def user_add():
    data        = request.get_json() or dict()
    name        = data.get('name', str())
    email       = data.get('email', str())
    password    = data.get('password', str())

    if not name:     raise BadRequest("Name required")
    if not email:    raise BadRequest("Email required")
    if not password: raise BadRequest("Password required")

    user = User(name=name, email=email, password=password)

    if 'account_ids' in data.keys():
        users.accounts = Account.query.filter(Account.id.in_(data['account_ids'])).all()

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return {"data": user.to_dict()}


@app.route('/api/1/users/<user_id>/', methods=['GET'])
@as_json
def user_show(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user: raise NotFound("No user exists with id '%s'" % user_id)
    return {"data": user.to_dict()}


@app.route('/api/1/users/<user_id>/', methods=['POST'])
@as_json
def user_update(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user: raise NotFound("No user exists with id '%s'" % user_id)

    data = request.get_json() or dict()
    if 'name'     in data.keys(): user.name     = data['name']
    if 'email'    in data.keys(): user.email    = data['email']
    if 'password' in data.keys(): user.password = data['password']
    if 'enabled'  in data.keys(): user.enabled  = data['enabled']
    if 'admin'    in data.keys(): user.admin    = data['admin']
    
    if 'account_ids' in data.keys():
        users.accounts = Account.query.filter(Account.id.in_(data['account_ids'])).all()

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return {"data": user.to_dict()}


@app.route('/api/1/users/<user_id>/', methods=['DELETE'])
@as_json
def user_delete(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user: raise NotFound("No user exists with id '%s'" % user_id)

    db.session.delete(user)
    db.session.commit()
    return {"data": "User (%s) deleted" % user_id}