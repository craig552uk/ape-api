# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing segments

from app import app, db
from app.models import *


@app.route('/api/1/segments/', methods=['GET'])
def segment_list():
    return "GET: List all segments"


@app.route('/api/1/segments/', methods=['POST'])
def segment_add():
    return "POST: Add an segment"


@app.route('/api/1/segments/<segment_id>/', methods=['GET'])
def segment_show(segment_id):
    return "GET: Show %s" % segment_id


@app.route('/api/1/segments/<segment_id>/', methods=['POST'])
def segment_update(segment_id):
    return "POST: Update %s" % segment_id


@app.route('/api/1/segments/<segment_id>/', methods=['DELETE'])
def segment_delete(segment_id):
    return "DELETE: Delete %s" % segment_id