# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Factory for generating sample data

from time import time as epoch

def make_pageview():
    """Return a valid visitor pageview object"""
    pv = dict()
    pv['page_url']         = "http://example.com"
    pv['referrer_url']     = "http://example.com"
    pv['page_title']       = "Foo Bar"
    pv['timestamp']        = epoch()
    pv['language']         = "en-GB"
    pv['event']            = "pageload"
    pv['placeholders']     = ['a', 'b', 'c`']
    pv['prefix']           = "ape"
    pv['script_version']   = "0.0.0"
    return pv

def make_session():
    """Return a valid visitor session object"""
    sn = dict()
    sn['session_start']    = epoch()
    sn['session_end']      = epoch()
    sn['session_duration'] = 100
    sn['request_address']  = "http://example.com"
    sn['user_agent']       = "FooBar"
    sn['screen_color']     = 256
    sn['screen_width']     = 1000
    sn['screen_height']    = 1000
    sn['pageviews']        = [make_pageview()]
    sn['pageview_count']   = 1
    return sn

def make_visitor_data():
    """Return a valid visitor data object"""
    data = dict()
    data['visitor_id']     = ""
    data['account_id']     = ""
    data['sessions']       = {0:make_session()}
    data['sessions_count'] = 1
    return data