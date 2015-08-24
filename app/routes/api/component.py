# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing components

from app import app, db
from app.models import *
from flask_json import as_json


@app.route('/api/1/placeholders/<placeholder_id>/components/', methods=['GET'])
@as_json
def component_list(placeholder_id):
    return {"message": "GET: List all Components for Placeholder %s" % placeholder_id}


@app.route('/api/1/placeholders/<placeholder_id>/components/', methods=['POST'])
@as_json
def component_add(placeholder_id):
    return {"message": "POST: Add a Component to Placeholder %s" % placeholder_id}


@app.route('/api/1/placeholders/<placeholder_id>/components/<component_id>/', methods=['GET'])
@as_json
def component_show(placeholder_id, component_id):
    return {"message": "GET: Show Component %s for Placeholder %s" % (component_id, placeholder_id)}


@app.route('/api/1/placeholders/<placeholder_id>/components/<component_id>/', methods=['POST'])
@as_json
def component_update(placeholder_id, component_id):
    return {"message": "POST: Update Component %s for Placeholder %s" % (component_id, placeholder_id)}


@app.route('/api/1/placeholders/<placeholder_id>/components/<component_id>/', methods=['DELETE'])
@as_json
def component_delete(placeholder_id, component_id):
    return {"message": "DELETE: Delete Component %s for Placeholder %s" % (component_id, placeholder_id)}