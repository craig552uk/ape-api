# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# URL routes for apps

import simplejson as json
from time import time as epoch
from app import app, db
from app.models import *
from flask import request, make_response
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError, Conflict

def jsonp_response(payload, code=200):
    """Make and return a jsonp response object"""
    body = '_ape.callback' + json.dumps(payload, indent=2) + ')'
    response = make_response(body, code)
    response.headers['Content-Type'] = "application/javascript;charset=utf-8"
    return response

@app.route('/beacon.js')
def beacon():

    # Respect Do Not Track
    if request.headers.get('DNT', False):
        raise Conflict("Do Not Track enabled on client")

    # Get args data or defaults
    args = dict()
    args['visitor_id']     = request.args.get('cc', "")      # The APE cookie visitor_id
    args['debug']          = request.args.get('db', "")      # Debug switch
    args['page_url']       = request.args.get('dl', "")      # Page URL
    args['referrer_url']   = request.args.get('dr', "")      # Referrer URL if set
    args['page_title']     = request.args.get('dt', "")      # Page title
    args['event']          = request.args.get('ev', "")      # Event
    args['customer_id']    = request.args.get('id', "")      # The customer account ID
    args['timestamp']      = request.args.get('ld', epoch()) # Epoch timestamp
    args['language']       = request.args.get('lg', "")      # Browser language
    args['placeholders']   = request.args.get('pc', "")      # The set of Placeholder ids on this page
    args['prefix']         = request.args.get('px', "ape")   # Placeholder class prefix
    args['screen_colour']  = request.args.get('sc', 0)       # Screen colour depth
    args['screen_height']  = request.args.get('sh', 0)       # Screen height
    args['screen_width']   = request.args.get('sw', 0)       # Screen width
    args['user_agent']     = request.args.get('ua', "")      # User Agent
    args['script_version'] = request.args.get('vr', "0.0.0") # Version number of this script

    # Convert values to base data types or defaults
    try:    args['screen_width']  = int(args['screen_width'])
    except: args['screen_width']  = 0

    try:    args['screen_height'] = int(args['screen_height'])
    except: args['screen_height'] = 0

    try:    args['screen_colour'] = int(args['screen_colour'])
    except: args['screen_colour'] = 0

    try:    args['timestamp']     = float(args['timestamp'])
    except: args['timestamp']     = epoch()

    try:    args['debug']         = (args['debug'].lower() == "true")
    except: args['debug']         = False

    # Ensure page url and customer id are provided
    if not args['page_url']:    raise BadRequest("Bad Request: Value required for page url (dl)")
    if not args['customer_id']: raise BadRequest("Bad Request: Value required for customer id (id)")

    # Extract placeholder identifiers
    placeholders = args['placeholders'].split(' ')
    prefix = args['prefix'] + "-"
    args['placeholder_ids'] = [c.lstrip(prefix) for c in placeholders if c.startswith(prefix)]

    # Response payload
    payload = dict()

    # Return args in payload in debug mode
    if args['debug']:
        payload['args'] = args

    # TODO Magic!

    return jsonp_response(payload)
    

@app.errorhandler(HTTPException)
def handle_error(e):
    payload  = {'error': e.description, 'name':  e.name}
    return jsonp_response(payload, e.code)
