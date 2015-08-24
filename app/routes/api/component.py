# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# API endpoints for managing components

from app import app, db
from app.models import *


@app.route('/api/1/placeholders/<placeholder_id>/components/', methods=['GET'])
def component_list(placeholder_id):
    return "GET: List all Components for Placeholder %s" % placeholder_id


@app.route('/api/1/placeholders/<placeholder_id>/components/', methods=['POST'])
def component_add(placeholder_id):
    return "POST: Add a Component to Placeholder %s" % placeholder_id


@app.route('/api/1/placeholders/<placeholder_id>/components/<component_id>/', methods=['GET'])
def component_show(placeholder_id, component_id):
    return "GET: Show Component %s for Placeholder %s" % (component_id, placeholder_id)


@app.route('/api/1/placeholders/<placeholder_id>/components/<component_id>/', methods=['POST'])
def component_update(placeholder_id, component_id):
    return "POST: Update Component %s for Placeholder %s" % (component_id, placeholder_id)


@app.route('/api/1/placeholders/<placeholder_id>/components/<component_id>/', methods=['DELETE'])
def component_delete(placeholder_id, component_id):
    return "DELETE: Delete Component %s for Placeholder %s" % (component_id, placeholder_id)