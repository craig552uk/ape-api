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

    # Get values from request object
    args = dict()
    args['user_agent']      = request.user_agent.string       # Full UserAgent string
    args['platform_name']   = request.user_agent.platform     # Platform name from UA
    args['browser_name']    = request.user_agent.browser      # Browser name from UA
    args['browser_version'] = request.user_agent.version      # Browser version from UA
    args['request_address'] = request.remote_addr             # Request IP address

    # Get args data or defaults
    args['visitor_id']      = request.args.get('cc', "")      # The APE cookie visitor_id
    args['debug']           = request.args.get('db', "")      # Debug switch
    args['page_url']        = request.args.get('dl', "")      # Page URL
    args['referrer_url']    = request.args.get('dr', "")      # Referrer URL if set
    args['page_title']      = request.args.get('dt', "")      # Page title
    args['event']           = request.args.get('ev', "")      # Event
    args['account_id']      = request.args.get('id', "")      # The customer account ID
    args['timestamp']       = request.args.get('ld', epoch()) # Epoch timestamp
    args['language']        = request.args.get('lg', "")      # Browser language
    args['placeholders']    = request.args.get('pc', "")      # The set of Placeholder ids on this page
    args['prefix']          = request.args.get('px', "ape")   # Placeholder class prefix
    args['screen_color']    = request.args.get('sc', 0)       # Screen colour depth
    args['screen_height']   = request.args.get('sh', 0)       # Screen height
    args['screen_width']    = request.args.get('sw', 0)       # Screen width
    args['script_version']  = request.args.get('vr', "0.0.0") # Version number of this script

    # Convert values to base data types or defaults
    try:    args['screen_width']  = int(args['screen_width'])
    except: args['screen_width']  = 0

    try:    args['screen_height'] = int(args['screen_height'])
    except: args['screen_height'] = 0

    try:    args['screen_color']  = int(args['screen_color'])
    except: args['screen_color']  = 0

    try:    args['timestamp']     = float(args['timestamp'])
    except: args['timestamp']     = epoch()

    try:    args['debug']         = (args['debug'].lower() == "true")
    except: args['debug']         = False

    # Ensure page url and customer id are provided
    if not args['page_url']:   raise BadRequest("Bad Request: Value required for page url (dl)")
    if not args['account_id']: raise BadRequest("Bad Request: Value required for customer id (id)")

    # Extract placeholder identifiers
    placeholders = args['placeholders'].split(' ')
    prefix = args['prefix'] + "-"
    args['placeholder_ids'] = [c.lstrip(prefix) for c in placeholders if c.startswith(prefix)]

    # Response payload
    payload = dict()

    # Return args in payload in debug mode
    if args['debug']:
        payload['args'] = args

    # Get account
    account = Account.query.filter_by(uuid=args['account_id']).first()
    if account:

        # Ensure account is enabled and valid for this page
        if account.enabled and account.url_in_sites(args['page_url']):

            # Get/create visitor record for this customer
            visitor = Visitor.get_or_create(account, args['visitor_id'])

            # Update visitor data with payload
            visitor_data = visitor.store_payload(args)

            # Ensure we have placeholder ids
            if args['placeholder_ids']:

                # Build list of applicable segments for visitor
                visitor_segments = [s for s in account.segments if s.matches_data(visitor_data)]

                if args['debug']:
                    # Add list of segment ids to payload
                    payload['segment_names'] = [s.name for s in visitor_segments]

                # Format components for json response
                payload['components'] = dict()
                for placeholder in account.placeholders:
                    key = "%s-%s" % (args['prefix'], placeholder.uuid)
                    component = placeholder.get_component_for_segments(segments)
                    if component:
                        payload['components'][key] = dict()
                        payload['components'][key]['content'] = component.markup

    return jsonp_response(payload)
    

@app.errorhandler(HTTPException)
def handle_error(e):
    payload  = {'error': e.description, 'name':  e.name}
    return jsonp_response(payload, e.code)
