# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing segments

from app import app, db
from app.models import *
from flask_json import as_json


@app.route('/api/1/segments/', methods=['GET'])
@as_json
def segment_list():
    return {"message": "GET: List all segments"}


@app.route('/api/1/segments/', methods=['POST'])
@as_json
def segment_add():
    return {"message": "POST: Add an segment"}


@app.route('/api/1/segments/<segment_id>/', methods=['GET'])
@as_json
def segment_show(segment_id):
    return {"message": "GET: Show %s" % segment_id}


@app.route('/api/1/segments/<segment_id>/', methods=['POST'])
@as_json
def segment_update(segment_id):
    return {"message": "POST: Update %s" % segment_id}


@app.route('/api/1/segments/<segment_id>/', methods=['DELETE'])
@as_json
def segment_delete(segment_id):
    return {"message": "DELETE: Delete %s" % segment_id}