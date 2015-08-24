# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing placeholders

from app import app, db
from app.models import *


@app.route('/api/1/placeholders/', methods=['GET'])
def placeholder_list():
    return "GET: List all placeholders"


@app.route('/api/1/placeholders/', methods=['POST'])
def placeholder_add():
    return "POST: Add a placeholder"


@app.route('/api/1/placeholders/<placeholder_id>/', methods=['GET'])
def placeholder_show(placeholder_id):
    return "GET: Show %s" % placeholder_id


@app.route('/api/1/placeholders/<placeholder_id>/', methods=['POST'])
def placeholder_update(placeholder_id):
    return "POST: Update %s" % placeholder_id


@app.route('/api/1/placeholders/<placeholder_id>/', methods=['DELETE'])
def placeholder_delete(placeholder_id):
    return "DELETE: Delete %s" % placeholder_id