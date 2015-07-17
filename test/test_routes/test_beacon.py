# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for app

import unittest
import simplejson as json
from app import app
from urllib import urlencode

# Mapping of friendly and short param names
params = {
    'visitor_id':     'cc', # The APE cookie visitor_id
    'debug':          'db', # Debug switch
    'page_url':       'dl', # Page URL
    'referrer_url':   'dr', # Referrer URL if set
    'page_title':     'dt', # Page title
    'event':          'ev', # Event
    'customer_id':    'id', # The customer account ID
    'timestamp':      'ld', # Event timestamp
    'language':       'lg', # Browser language
    'placeholders':   'pc', # The set of Placeholder ids on this page
    'prefix':         'px', # Placeholder class prefix
    'screen_colour':  'sc', # Screen colour depth
    'screen_height':  'sh', # Screen height
    'screen_width':   'sw', # Screen width
    'user_agent':     'ua', # User Agent
    'script_version': 'vr', # Version number of this script
}

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def get_beacon(self, **kwargs):
        """Assert and unpack beacon response"""

        # Use defaults if not provided
        if not 'debug' in kwargs.keys():       kwargs['debug']       = True
        if not 'page_url' in kwargs.keys():    kwargs['page_url']    = "http://example.com"
        if not 'customer_id' in kwargs.keys(): kwargs['customer_id'] = "foo-bar"

        # Map frindly params to short names
        args = {params[key]: val for key,val in kwargs.items()}
        r = self.app.get('/beacon.js?' + urlencode(args))

        self.assertEqual(r.mimetype, "application/javascript")
        self.assertEqual(r.status_code, 200)
        
        data = json.loads(r.data)
        self.assertIsInstance(data, dict)
        return data

    def test_do_not_track(self):
        # Should respect Do Not Track header
        r = self.app.get('/beacon.js?', headers=[('DNT', 'true')])
        self.assertEqual(r.mimetype, "application/javascript")
        self.assertEqual(r.status_code, 409) # Conflict
        self.assertIsInstance(json.loads(r.data), dict)

    def test_beacon_page_url(self):
        value = "http://example.com?foo=bar#baz"
        data = self.get_beacon(page_url=value)
        self.assertIn('page_url', data['args'])
        self.assertEqual(value, data['args']['page_url'])

        # Without page_url
        r = self.app.get('/beacon.js?id=foo')
        self.assertEqual(r.mimetype, "application/javascript")
        self.assertEqual(r.status_code, 400) # Bad Request
        self.assertIsInstance(json.loads(r.data), dict)

    def test_beacon_customer_id(self):
        value = "foo-bar"
        data = self.get_beacon(customer_id=value)
        self.assertIn('customer_id', data['args'])
        self.assertEqual(value, data['args']['customer_id'])
        
        # Without customer_id
        r = self.app.get('/beacon.js?dl=foo')
        self.assertEqual(r.mimetype, "application/javascript")
        self.assertEqual(r.status_code, 400) # Bad Request
        self.assertIsInstance(json.loads(r.data), dict)

    def test_beacon_debug(self):
        # debug off
        data = self.get_beacon(debug=False)
        self.assertNotIn('args', data)

        # debug on
        data = self.get_beacon(debug=True)
        self.assertIn('args', data)
        self.assertTrue(data['args']['debug'])

    def test_beacon_visitor_id(self):
        value = "foo-bar"
        data = self.get_beacon(visitor_id=value)
        self.assertIn('visitor_id', data['args'])
        self.assertEqual(value, data['args']['visitor_id'])

    def test_beacon_referrer_url(self):
        value = "http://example.com?foo=bar#baz"
        data = self.get_beacon(referrer_url=value)
        self.assertIn('referrer_url', data['args'])
        self.assertEqual(value, data['args']['referrer_url'])

    def test_beacon_page_title(self):
        value = "Foo Bar"
        data = self.get_beacon(page_title=value)
        self.assertIn('page_title', data['args'])
        self.assertEqual(value, data['args']['page_title'])

    def test_beacon_event(self):
        value = "foobar"
        data = self.get_beacon(event=value)
        self.assertIn('event', data['args'])
        self.assertEqual(value, data['args']['event'])

    def test_beacon_timestamp(self):
        value = 1437139273.55 # urlencode rounds floats to 2dp
        data = self.get_beacon(timestamp=value)
        self.assertIn('timestamp', data['args'])
        self.assertEqual(value, data['args']['timestamp'])

        # Bad Value
        data = self.get_beacon(timestamp="foo")
        self.assertIsInstance(data['args']['timestamp'], float)

    def test_beacon_language(self):
        value = "en_gb"
        data = self.get_beacon(language=value)
        self.assertIn('language', data['args'])
        self.assertEqual(value, data['args']['language'])

    def test_beacon_placeholders(self):
        value = "foo-bar ape-baz"
        data = self.get_beacon(placeholders=value)
        self.assertIn('placeholders', data['args'])
        self.assertEqual(value, data['args']['placeholders'])

        # Extracted placeholder ids (prefixed with "ape")
        self.assertEqual(['baz'], data['args']['placeholder_ids'])

    def test_beacon_prefix(self):
        value = "foobar"
        data = self.get_beacon(prefix=value)
        self.assertIn('prefix', data['args'])
        self.assertEqual(value, data['args']['prefix'])

    def test_beacon_screen_colour(self):
        value = 64
        data = self.get_beacon(screen_colour=value)
        self.assertIn('screen_colour', data['args'])
        self.assertEqual(value, data['args']['screen_colour'])

        # Bad Value
        data = self.get_beacon(screen_colour="foo")
        self.assertEqual(0, data['args']['screen_height'])

    def test_beacon_screen_height(self):
        value = 720
        data = self.get_beacon(screen_height=value)
        self.assertIn('screen_height', data['args'])
        self.assertEqual(value, data['args']['screen_height'])
        
        # Bad Value
        data = self.get_beacon(screen_height="foo")
        self.assertEqual(0, data['args']['screen_height'])

    def test_beacon_screen_width(self):
        value = 1280
        data = self.get_beacon(screen_width=value)
        self.assertIn('screen_width', data['args'])
        self.assertEqual(value, data['args']['screen_width'])
        
        # Bad Value
        data = self.get_beacon(screen_width="foo")
        self.assertEqual(0, data['args']['screen_width'])

    def test_beacon_user_agent(self):
        value = "Foo Bar"
        data = self.get_beacon(user_agent=value)
        self.assertIn('user_agent', data['args'])
        self.assertEqual(value, data['args']['user_agent'])

    def test_beacon_script_version(self):
        value = "0.0.0"
        data = self.get_beacon(script_version=value)
        self.assertIn('script_version', data['args'])
        self.assertEqual(value, data['args']['script_version'])
