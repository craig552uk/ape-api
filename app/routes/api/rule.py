# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing rules

from app import app, db
from app.models import *


@app.route('/api/1/segments/<segment_id>/rules/', methods=['GET'])
def rule_list(segment_id):
    return "GET: List all Rules for Segment %s" % segment_id


@app.route('/api/1/segments/<segment_id>/rules/', methods=['POST'])
def rule_add(segment_id):
    return "POST: Add a Rule to Segment %s" % segment_id


@app.route('/api/1/segments/<segment_id>/rules/<rule_id>/', methods=['GET'])
def rule_show(segment_id, rule_id):
    return "GET: Show Rule %s for Segment %s" % (rule_id, segment_id)


@app.route('/api/1/segments/<segment_id>/rules/<rule_id>/', methods=['POST'])
def rule_update(segment_id, rule_id):
    return "POST: Update Rule %s for Segment %s" % (rule_id, segment_id)


@app.route('/api/1/segments/<segment_id>/rules/<rule_id>/', methods=['DELETE'])
def rule_delete(segment_id, rule_id):
    return "DELETE: Delete Rule %s for Segment %s" % (rule_id, segment_id)