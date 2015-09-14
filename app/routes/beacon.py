# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# URL routes for apps

from time import time as epoch
from app import app, db, json_app
from app.models import *
from flask import request
from flask_json import as_json, json_response
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError, Conflict


# If set, response uses JSONP
# TODO Use app config perhaps?
JSONP_CALLBACK = None


def jsonp_response(data, status=200, headers=None):
    """
        Build jsonp response if global var set
        Return standard json response otherwise
        # TODO move in to flask_json library
    """
    response = json_response(status_=status, headers_=headers, **data)
    if (JSONP_CALLBACK):
        response.status_code = 200
        response.headers['Content-Type'] = "application/javascript"
        response.data = JSONP_CALLBACK % response.data
    return response


@app.route('/beacon.js')
def beacon():
   
    # Global JSONP callback value ensures JSONP response
    global JSONP_CALLBACK
    JSONP_CALLBACK = "_ape.callback(%s)"

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
    if not args['page_url']:   raise BadRequest("Value required for page url (dl)")
    if not args['account_id']: raise BadRequest("Value required for customer id (id)")

    # Extract placeholder identifiers
    placeholders = args['placeholders'].split(' ')
    prefix = args['prefix'] + "-"
    args['placeholder_ids'] = [c.lstrip(prefix) for c in placeholders if c.startswith(prefix)]

    # Response payload
    payload = dict()

    # Return args in payload in debug mode
    if args['debug']:
        payload['args'] = args
        # TODO Add timings to response

    # Get account
    account = Account.query.filter_by(uuid=args['account_id']).first()
    if account:

        # Ensure account is enabled and valid for this page
        if account.enabled and account.url_in_sites(args['page_url']):

            # Get/create visitor record for this customer
            visitor = Visitor.get_or_create(account, args['visitor_id'])
            payload['visitor_id'] = visitor.uuid

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

                    # Ignore unrequested placeholders
                    if placeholder.uuid in args['placeholder_ids']:
                       
                        key = "%s-%s" % (args['prefix'], placeholder.uuid)
                        component = placeholder.get_component_for_segments(visitor_segments)
                        if component:
                            payload['components'][key] = dict()
                            payload['components'][key]['content'] = component.markup
    
    return jsonp_response(payload)
    

# TODO move exceptions to home.py or dedicated module

@app.errorhandler(HTTPException)
def handle_error(e):
    error = dict(title=e.name, status=str(e.code), detail=e.description)
    return jsonp_response({'error': error}, e.code)


@json_app.invalid_json_error
@as_json
def invalid_json_error(e):
    raise BadRequest("Invalid JSON")