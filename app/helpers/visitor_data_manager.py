# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Visitor Data Management utiltiies

from time import time as epoch
from copy import deepcopy


def append_payload(payload, data):
    """Returns dict with payload data correctly inserted"""

    # Set intial values if required
    if 'visitor_id' not in data: data['visitor_id'] = payload.get('visitor_id', None)
    if 'account_id' not in data: data['account_id'] = payload.get('account_id', None)
    if 'sessions'   not in data: data['sessions']   = dict()

    num_sessions = len(data['sessions'])

    if num_sessions == 0:
        data['sessions'][0] = new_session(payload)
    else:
        last_session = data['sessions'][num_sessions-1]
        if payload_is_part_of_session(payload, last_session):
            data['sessions'][num_sessions-1] = update_session(payload, last_session)
        else:
            data['sessions'][num_sessions] = new_session(payload)

    # Set derived values
    data['session_count'] = len(data['sessions'])
    return data


def new_session(payload):
    """Return a new session from payload data"""
    session = dict()
    session['session_start']    = payload.get('timestamp', epoch())
    session['session_end']      = payload.get('timestamp', epoch())
    session['session_duration'] = 0
    session['request_address']  = payload.get('request_address', None)
    # TODO country, city etc from ip address
    session['user_agent']       = payload.get('user_agent', None)
    session['screen_color']     = payload.get('screen_color', None)
    session['screen_width']     = payload.get('screen_width', None)
    session['screen_height']    = payload.get('screen_height', None)
    session['pageviews'] = list()
    session['pageviews'].append(new_pageview(payload))
    session['pageview_count']   = 1
    return session


def update_session(payload, session):
    """Update the session with the payload data"""
    # Using deep copy to prevent accidental data pollution
    session = deepcopy(session)
    session['session_end']      = payload.get('timestamp', epoch())
    session['session_duration'] = session['session_end'] - session['session_start']
    session['pageviews'].append(new_pageview(payload))
    session['pageview_count']   = len(session['pageviews'])
    return session


def new_pageview(payload):
    """Return a new pageview record from the payload"""
    pageview = dict()
    pageview['page_url']       = payload.get('page_url', None)
    pageview['referrer_url']   = payload.get('referrer_url', None)
    pageview['page_title']     = payload.get('page_title', None)
    pageview['event']          = payload.get('event', None)
    pageview['timestamp']      = payload.get('timestamp', None)
    pageview['language']       = payload.get('language', None)
    pageview['placeholders']   = payload.get('placeholders', None)
    pageview['prefix']         = payload.get('prefix', None)
    pageview['script_version'] = payload.get('script_version', None)
    return pageview


def payload_is_part_of_session(payload, session):
    """
        True if request address and user agent are the same
        and timestamp difference is less than 30 minutes
    """
    return session.get('request_address', "X") == payload.get('request_address', "") \
       and session.get('user_agent', "X")      == payload.get('user_agent', "") \
       and session.get('session_end', 0)       >= payload.get('timestamp', 0) - (30*60)