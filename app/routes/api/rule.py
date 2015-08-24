# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing rules

from app import app, db
from app.models import *
from flask_json import as_json


@app.route('/api/1/segments/<segment_id>/rules/', methods=['GET'])
@as_json
def rule_list(segment_id):
    return {"message": "GET: List all Rules for Segment %s" % segment_id}


@app.route('/api/1/segments/<segment_id>/rules/', methods=['POST'])
@as_json
def rule_add(segment_id):
    return {"message": "POST: Add a Rule to Segment %s" % segment_id}


@app.route('/api/1/segments/<segment_id>/rules/<rule_id>/', methods=['GET'])
@as_json
def rule_show(segment_id, rule_id):
    return {"message": "GET: Show Rule %s for Segment %s" % (rule_id, segment_id)}


@app.route('/api/1/segments/<segment_id>/rules/<rule_id>/', methods=['POST'])
@as_json
def rule_update(segment_id, rule_id):
    return {"message": "POST: Update Rule %s for Segment %s" % (rule_id, segment_id)}


@app.route('/api/1/segments/<segment_id>/rules/<rule_id>/', methods=['DELETE'])
@as_json
def rule_delete(segment_id, rule_id):
    return {"message": "DELETE: Delete Rule %s for Segment %s" % (rule_id, segment_id)}