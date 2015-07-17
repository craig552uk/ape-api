# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Unit Tests for app

import time
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
        args = {params[key]: val for key,val in kwargs.items()}
        r = self.app.get('/beacon.js?' + urlencode(args))

        self.assertEqual(r.mimetype, "application/javascript")
        self.assertEqual(r.status_code, 200)
        
        data = json.loads(r.data)
        self.assertIsInstance(data, dict)
        return data

    def test_beacon_debug(self):
        # debug not provided
        data = self.get_beacon()
        self.assertNotIn('args', data)

        # debug data provided
        data = self.get_beacon(debug=True)
        self.assertIn('args', data)

        # Debug provides all params
        for param in params.keys():
            self.assertIn(param, data['args'])

        # Debug flag is set (obvs!)
        self.assertTrue(data['args']['debug'])

    def test_beacon_visitor_id(self):
        value = "foo-bar"
        data = self.get_beacon(debug=True, visitor_id=value)
        self.assertIn('visitor_id', data['args'])
        self.assertEqual(value, data['args']['visitor_id'])

    def test_beacon_page_url(self):
        value = "http://example.com?foo=bar#baz"
        data = self.get_beacon(debug=True, page_url=value)
        self.assertIn('page_url', data['args'])
        self.assertEqual(value, data['args']['page_url'])

    def test_beacon_referrer_url(self):
        value = "http://example.com?foo=bar#baz"
        data = self.get_beacon(debug=True, referrer_url=value)
        self.assertIn('referrer_url', data['args'])
        self.assertEqual(value, data['args']['referrer_url'])

    def test_beacon_page_title(self):
        value = "Foo Bar"
        data = self.get_beacon(debug=True, page_title=value)
        self.assertIn('page_title', data['args'])
        self.assertEqual(value, data['args']['page_title'])

    def test_beacon_event(self):
        value = "foobar"
        data = self.get_beacon(debug=True, event=value)
        self.assertIn('event', data['args'])
        self.assertEqual(value, data['args']['event'])

    def test_beacon_customer_id(self):
        value = "foo-bar"
        data = self.get_beacon(debug=True, customer_id=value)
        self.assertIn('customer_id', data['args'])
        self.assertEqual(value, data['args']['customer_id'])

    def test_beacon_timestamp(self):
        value = int(time.time())
        data = self.get_beacon(debug=True, timestamp=value)
        self.assertIn('timestamp', data['args'])
        self.assertEqual(value, data['args']['timestamp'])

        # Bad Value
        data = self.get_beacon(debug=True, timestamp="foo")
        self.assertIsInstance(data['args']['screen_height'], int)

    def test_beacon_language(self):
        value = "en_gb"
        data = self.get_beacon(debug=True, language=value)
        self.assertIn('language', data['args'])
        self.assertEqual(value, data['args']['language'])

    def test_beacon_placeholders(self):
        value = "foo bar baz"
        data = self.get_beacon(debug=True, placeholders=value)
        self.assertIn('placeholders', data['args'])
        self.assertEqual(value, data['args']['placeholders'])

    def test_beacon_prefix(self):
        value = "foobar"
        data = self.get_beacon(debug=True, prefix=value)
        self.assertIn('prefix', data['args'])
        self.assertEqual(value, data['args']['prefix'])

    def test_beacon_screen_colour(self):
        value = 64
        data = self.get_beacon(debug=True, screen_colour=value)
        self.assertIn('screen_colour', data['args'])
        self.assertEqual(value, data['args']['screen_colour'])

        # Bad Value
        data = self.get_beacon(debug=True, screen_colour="foo")
        self.assertEqual(0, data['args']['screen_height'])

    def test_beacon_screen_height(self):
        value = 720
        data = self.get_beacon(debug=True, screen_height=value)
        self.assertIn('screen_height', data['args'])
        self.assertEqual(value, data['args']['screen_height'])
        
        # Bad Value
        data = self.get_beacon(debug=True, screen_height="foo")
        self.assertEqual(0, data['args']['screen_height'])


    def test_beacon_screen_width(self):
        value = 1280
        data = self.get_beacon(debug=True, screen_width=value)
        self.assertIn('screen_width', data['args'])
        self.assertEqual(value, data['args']['screen_width'])
        
        # Bad Value
        data = self.get_beacon(debug=True, screen_width="foo")
        self.assertEqual(0, data['args']['screen_width'])


    def test_beacon_user_agent(self):
        value = "Foo Bar"
        data = self.get_beacon(debug=True, user_agent=value)
        self.assertIn('user_agent', data['args'])
        self.assertEqual(value, data['args']['user_agent'])

    def test_beacon_script_version(self):
        value = "0.0.0"
        data = self.get_beacon(debug=True, script_version=value)
        self.assertIn('script_version', data['args'])
        self.assertEqual(value, data['args']['script_version'])
