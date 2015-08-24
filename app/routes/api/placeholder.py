# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing placeholders

from app import app, db
from app.models import *
from flask_json import as_json


@app.route('/api/1/placeholders/', methods=['GET'])
@as_json
def placeholder_list():
    return {"message": "GET: List all placeholders"}


@app.route('/api/1/placeholders/', methods=['POST'])
@as_json
def placeholder_add():
    return {"message": "POST: Add a placeholder"}


@app.route('/api/1/placeholders/<placeholder_id>/', methods=['GET'])
@as_json
def placeholder_show(placeholder_id):
    return {"message": "GET: Show %s" % placeholder_id}


@app.route('/api/1/placeholders/<placeholder_id>/', methods=['POST'])
@as_json
def placeholder_update(placeholder_id):
    return {"message": "POST: Update %s" % placeholder_id}


@app.route('/api/1/placeholders/<placeholder_id>/', methods=['DELETE'])
@as_json
def placeholder_delete(placeholder_id):
    return {"message": "DELETE: Delete %s" % placeholder_id}